import hata
import hata.ext.patchouli
import hata.ext.plugin_loader
import hata.ext.slash
import hata.ext.commands_v2
import hata.ext.commands_v2.helps.subterranean
import hata.ext.top_gg
import hata.ext.solarlink
import scarletio
import scarletio.http_client

from hata.ext.patchouli import map_module, MAPPED_OBJECTS, ModuleUnit, QualPath, FunctionUnit, ClassAttributeUnit, \
    InstanceAttributeUnit, TypeUnit, PropertyUnit, search_paths, set_highlight_html_class, highlight

map_module('hata')
map_module('scarletio')

from flask import Blueprint, render_template, redirect, url_for, request, jsonify

from .forms import SearchForm
from .utils import get_back_path, get_searched_info, UNIT_TYPE_ORDER_PRIORITY_TYPE, build_js_structure, \
    build_html_structure, search_info_sort_key

URL_PREFIX = '/project/hata/docs'
ROUTES = Blueprint('docs', '', url_prefix=URL_PREFIX)


set_highlight_html_class(highlight.TOKEN_TYPE_SPECIAL_OPERATOR, 'c_py_operator')
set_highlight_html_class(highlight.TOKEN_TYPE_IDENTIFIER_MAGIC, 'c_py_magic')
set_highlight_html_class(highlight.TOKEN_TYPE_NUMERIC, 'c_py_numeric')
set_highlight_html_class(highlight.TOKEN_TYPE_STRING, 'c_py_string')
set_highlight_html_class(highlight.TOKEN_TYPE_IDENTIFIER_KEYWORD, 'c_py_keyword')
set_highlight_html_class(highlight.TOKEN_TYPE_IDENTIFIER_BUILTIN, 'c_py_builtin')
set_highlight_html_class(highlight.TOKEN_TYPE_IDENTIFIER_BUILTIN_EXCEPTION, 'c_py_builtin_exception')
set_highlight_html_class(highlight.TOKEN_TYPE_SPECIAL_PUNCTUATION, 'c_py_punctuation')
set_highlight_html_class(highlight.TOKEN_TYPE_SPECIAL_OPERATOR_ATTRIBUTE, 'c_py_operator_attribute')
set_highlight_html_class(highlight.TOKEN_TYPE_IDENTIFIER_ATTRIBUTE, 'c_py_identifier_attribute')
set_highlight_html_class(highlight.TOKEN_TYPE_SPECIAL_CONSOLE_PREFIX, 'c_py_identifier_console_prefix')
set_highlight_html_class(highlight.TOKEN_TYPE_STRING_UNICODE_FORMAT_MARK, 'c_py_format_string_mark')
set_highlight_html_class(highlight.TOKEN_TYPE_COMMENT, 'c_py_comment')
set_highlight_html_class(highlight.TOKEN_TYPE_STRING_UNICODE_FORMAT_CODE, 'c_py_format_string_code')
set_highlight_html_class(highlight.TOKEN_TYPE_STRING_UNICODE_FORMAT_POSTFIX, 'c_py_format_string_postfix')


class DocsWrapper:
    __slots__ = ('unit',)
    
    @property
    def __name__(self):
        return self.path
    
    def __init__(self, unit):
        self.unit = unit
    
    def __call__(self):
        search_form = SearchForm()
        unit = self.unit
        back_path = get_back_path(unit)
        content, structure = unit.html_extended_with_structure
        structure_html = build_html_structure(structure)
        structure_js = build_js_structure(structure)
        
        return render_template(
            'hata_docs_content.html',
            title = unit.name,
            content = content,
            search_form = search_form,
            back_path = back_path,
            structure_html = structure_html,
            structure_js = structure_js,
        )

class Redirecter:
    __slots__ = ('redirect_to')
    
    def __init__(self, redirect_to):
        self.redirect_to = redirect_to
    
    def __call__(self):
        return redirect(self.redirect_to)

ADDED_OBJECTS = set()

def unit_adder(unit):
    path = '/'+'/'.join(unit.path.parts)
    ROUTES.add_url_rule(path, path, DocsWrapper(unit))
    
    path += '/'
    ROUTES.add_url_rule(path, path, Redirecter('../' + unit.path.parts[-1]))
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

scarletio_module = MAPPED_OBJECTS['scarletio']
unit_adder(scarletio_module)
recursive_unit_adder(scarletio_module)

del unit_adder
del recursive_unit_adder
del ADDED_OBJECTS
del hata_module
del scarletio_module


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
            found.sort(key=search_info_sort_key)
            
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
    
    search_for = query_parameters.get('search_for', None)
    limit = query_parameters.get('limit', None)
    
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
        found.sort(key=search_info_sort_key)
        
        for order_priority, name, url, type_, preview in found:
            element = {
                'name': name,
                'url': url,
                'type': type_,
            }
            
            if (preview is not None):
               element['preview'] = preview
            
            response.append(element)
    
    
    return jsonify(response)
