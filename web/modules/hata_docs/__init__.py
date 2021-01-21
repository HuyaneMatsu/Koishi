# -*- coding: utf-8 -*-
import hata
import hata.ext.patchouli
import hata.ext.extension_loader
import hata.ext.commands
import hata.ext.commands.helps.subterranean
import hata.ext.slash

from hata.ext.patchouli import map_module, MAPPED_OBJECTS, ModuleUnit, QualPath, FunctionUnit, ClassAttributeUnit, \
    InstanceAttributeUnit, TypeUnit, PropertyUnit, search_paths

map_module('hata')

from flask import Blueprint, render_template, redirect, url_for, request, jsonify

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
        search_for = search_form.query.data.strip()
        
        results = search_paths(search_for)
        
        if len(results) == 0:
            found = None
        else:
            if len(results) == 1:
                path = next(iter(results))
                url = get_searched_info(path)[2]
                return redirect(url)
            
            found = []
            for index, path in enumerate(results):
                found.append(get_searched_info(path, index))
            found.sort(key=lambda x: x[0])
            
            first = found[0]
            if first[3] == 'class' and first[1] == search_for:
                url = first[2]
                return redirect(url)
    
    else:
        found = None
    
    return render_template('hata_docs_search.html', search_form=search_form, found=found)


DEFAULT_LIMIT = 100

@ROUTES.route('api/v1/search')
def api_search():
    query_parameters = request.args
    
    search_for = query_parameters.get('search_for')
    limit = query_parameters.get('limit')
    
    response = []
    
    if (search_for is not None):
        if limit is None:
            limit = DEFAULT_LIMIT
        else:
            try:
                limit = int(limit)
            except ValueError:
                limit = DEFAULT_LIMIT
            else:
                if limit <= 0:
                    limit = DEFAULT_LIMIT
        
        found = []
        for index, path in  enumerate(search_paths(search_for, limit=limit)):
            found.append(get_searched_info(path, index))
        found.sort(key=lambda x: x[0])
        
        for order_prio, name, url, type_, preview in found:
            element = {
                'name' : name,
                'url' : url,
                'type' : type_,
                    }
            
            if (preview is not None):
               element['preview'] = preview
            
            response.append(element)
    
    
    return jsonify(response)
