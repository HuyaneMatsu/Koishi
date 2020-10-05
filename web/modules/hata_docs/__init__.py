# -*- coding: utf-8 -*-
import hata
import hata.ext.patchouli
import hata.ext.extension_loader
import hata.ext.commands

from hata.ext.patchouli import map_module, MAPPED_OBJECTS, ModuleUnit, QualPath, FunctionUnit, ClassAttributeUnit, \
    InstanceAttributeUnit, TypeUnit, PropertyUnit, search_paths

map_module('hata')

from flask import Blueprint, render_template, redirect, url_for

from .forms import SearchForm
from .utils import get_backpath, get_searched_info, UNIT_TYPE_ORDER_PRIO_TYPE, build_js_structure, build_html_structure

URL_PREFIX = '/docs'
ROUTES = Blueprint('docs', 'hata_docs', url_prefix=URL_PREFIX)

class DocsWrapper(object):
    __slots__ = ('path', 'unit',)
    
    @property
    def __name__(self):
        return self.path
    
    def __init__(self, path, unit):
        self.path = path
        self.unit = unit
    
    def __call__(self):
        search_form = SearchForm()
        unit = self.unit
        backpath = get_backpath(unit)
        content, structure = unit.html_extended_with_structure
        structure_html = build_html_structure(structure)
        structure_js = build_js_structure(structure)
        
        return render_template('hata_docs_content.html',
            title = unit.name,
            content = content,
            search_form = search_form,
            backpath = backpath,
            structure_html = structure_html,
            structure_js = structure_js,
                )

class Redirecter(object):
    __slots__ = ('path', 'redirect_to')
    
    @property
    def __name__(self):
        return self.path
    
    def __init__(self, path, redirect_to):
        self.path = path
        self.redirect_to = redirect_to
    
    def __call__(self):
        return redirect(self.redirect_to)

ADDED_OBJECTS = set()

def unit_adder(unit):
    path = '/'+'/'.join(unit.path.parts)
    ROUTES.route(path)(DocsWrapper(path, unit))
    
    path += '/'
    ROUTES.route(path)(Redirecter(path, '../'+unit.path.parts[-1]))
    
    ADDED_OBJECTS.add(unit)

def recursive_unit_adder(module_unit):
    for unit in module_unit.references.values():
        if unit in ADDED_OBJECTS:
            continue
        
        if type(unit) is ModuleUnit:
            recursive_unit_adder(unit)
        
        unit_adder(unit)

hata_module = MAPPED_OBJECTS['hata']
unit_adder(hata_module)
recursive_unit_adder(hata_module)

del unit_adder
del recursive_unit_adder
del ADDED_OBJECTS
del hata_module



@ROUTES.route('/search', methods=['GET', 'POST'])
def search():
    search_form = SearchForm()
    if search_form.validate_on_submit():
        search_for = search_form.query.data
        
        results = search_paths(search_for)
        
        if len(results) == 0:
            found = None
        else:
            if len(results) == 1:
                path = next(iter(results))
                url = get_searched_info(path)[2]
                return redirect(url)
            
            found = []
            for path in results:
                found.append(get_searched_info(path))
            found.sort()
            
            first = found[0]
            if first[0] == UNIT_TYPE_ORDER_PRIO_TYPE and first[1] == search_for:
                url = first[2]
                return redirect(url)
    
    else:
        found = None
    
    return render_template('hata_docs_search.html', search_form=search_form, found=found)
