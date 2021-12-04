from html import escape as html_escape

from scarletio.web_common import quote
from hata.ext.patchouli import map_module, MAPPED_OBJECTS, ModuleUnit, QualPath, FunctionUnit, ClassAttributeUnit, \
    InstanceAttributeUnit, TypeUnit, PropertyUnit, search_paths
from hata.ext.patchouli.parser import ATTRIBUTE_SECTION_NAME_RP

UNIT_TYPE_ORDER_PRIORITY_TYPE = 0

UNIT_TYPE_ORDER_PRIORITY_MODULE = 10

UNIT_TYPE_ORDER_PRIORITY_FUNCTION = 8
UNIT_TYPE_ORDER_PRIORITY_PROPERTY = 24
UNIT_TYPE_ORDER_PRIORITY_METHOD = 16

UNIT_TYPE_ORDER_PRIORITY_INSTANCE_ATTRIBUTE = 24
UNIT_TYPE_ORDER_PRIORITY_CLASS_ATTRIBUTE = 30

UNIT_TYPE_ORDER_PRIORITY_NONE = 40

UNIT_TYPE_ORDER_PRIORITY_TYPE_NAME_RELATION = {
    ModuleUnit : ('module', UNIT_TYPE_ORDER_PRIORITY_MODULE),
    TypeUnit : ('class', UNIT_TYPE_ORDER_PRIORITY_TYPE),
    PropertyUnit : ('property', UNIT_TYPE_ORDER_PRIORITY_PROPERTY),
    InstanceAttributeUnit : ('attribute', UNIT_TYPE_ORDER_PRIORITY_INSTANCE_ATTRIBUTE),
    ClassAttributeUnit : ('class attribute', UNIT_TYPE_ORDER_PRIORITY_CLASS_ATTRIBUTE),
}

CLASS_ATTRIBUTE_SECTION_PRIORITIES = {
    'Class Attributes' : 0,
    'Type Attributes' : 1,
    'Attributes' : 2,
    'Instance Attributes' : 3,
}

CLASS_ATTRIBUTE_SECTION_DEFAULT = 4

def get_back_path(unit):
    parts = [(unit.name, '#')]
    
    counter = 1
    while True:
        unit = unit.parent
        if unit is None:
            break
        
        parts.append((unit.name, '../'*counter+quote(unit.name)))
        counter += 1
        continue
    
    result = []
    index = len(parts)-1
    while True:
        name, url = parts[index]
        result.append('<a href="')
        result.append(url)
        result.append('">')
        result.append(html_escape(name))
        result.append('</a>')
        
        if index == 0:
            break
        
        index -= 1
        result.append(' / ')
        continue
    
    return ''.join(result)

def get_searched_info(path, order_priority_base=0):
    unit = MAPPED_OBJECTS.get(path, None)
    if unit is None:
        type_ = None
        order_priority = 100
    else:
        unit_type = type(unit)
        if unit_type is FunctionUnit:
            parent = path.parent
            parent_unit = MAPPED_OBJECTS.get(parent, None)
            if parent_unit is None:
                type_ = 'function'
                order_priority = UNIT_TYPE_ORDER_PRIORITY_FUNCTION
            elif type(parent_unit) is TypeUnit:
                type_ = 'method'
                order_priority = UNIT_TYPE_ORDER_PRIORITY_METHOD
            else:
                type_ = 'function'
                order_priority = UNIT_TYPE_ORDER_PRIORITY_FUNCTION
        else:
            try:
                type_, order_priority = UNIT_TYPE_ORDER_PRIORITY_TYPE_NAME_RELATION[unit_type]
            except KeyError:
                type_ = None
                order_priority = UNIT_TYPE_ORDER_PRIORITY_NONE
    
    backfetched = []
    while True:
        parent = path.parent
        parent_unit = MAPPED_OBJECTS.get(parent, None)
        if parent_unit is None:
            break
        
        if type(parent_unit) is ModuleUnit:
            break
        
        backfetched.append(path.parts[-1])
        path = parent
        continue
    
    url_parts = []
    name_parts = []
    
    parts = path.parts
    limit = len(parts)
    if limit:
        index = 0
        while True:
            part = parts[index]
            part = quote(part)
            url_parts.append(part)
            
            index += 1
            if index == limit:
                break
            
            url_parts.append('/')
        
        name_parts.append(parts[-1])
        
    index = len(backfetched)
    if index:
        url_parts.append('#')
        
        while True:
            index -=1
            part = backfetched[index]
            name_parts.append(part)
            
            part = part.lower().replace(' ', '-')
            part = quote(part)
            url_parts.append(part)
            
            if index == 0:
                break
            
            url_parts.append('-')
            continue
    
    name = '.'.join(name_parts)
    if order_priority == UNIT_TYPE_ORDER_PRIORITY_CLASS_ATTRIBUTE:
        while True:
            docs = unit.docs
            if (docs is None):
                fail = True
                break
            
            parent = unit.parent
            if (parent is None):
                fail = True
                break
                
            docs = parent.docs
            if (docs is None):
                fail = True
                break
                
            attribute_sections = []
            for section_name, section_parts in docs.sections:
                if section_name is None:
                    continue
                
                if ATTRIBUTE_SECTION_NAME_RP.fullmatch(section_name) is None:
                    continue
                
                attribute_sections.append(section_name)
                continue
            
            if not attribute_sections:
                fail = True
                break
            
            best_match_name = None
            best_match_priority = 100
            for attribute_section_name in attribute_sections:
                priority = CLASS_ATTRIBUTE_SECTION_PRIORITIES.get(attribute_section_name, CLASS_ATTRIBUTE_SECTION_DEFAULT)
                if priority < best_match_priority:
                    best_match_priority = priority
                    best_match_name = attribute_section_name
            
            url_parts[-1] = best_match_name.lower().replace(' ', '-')
            fail = False
            break
        
        if fail:
            del url_parts[-2:]
    
    url = ''.join(url_parts)
    if unit is None:
        preview = None
    else:
        preview = unit.preview
    return order_priority_base+order_priority, name, url, type_, preview


def search_info_sort_key(search_info):
    return search_info[0]


def build_js_structure(structure):
    parts = ['[']
    children = structure.children
    if (children is not None):
        for index, child in enumerate(children):
            parts.extend(build_js_structure_gen(child, f'ct_{index}'))
    
    parts.append(']')
    return ''.join(parts)

def build_js_structure_gen(structure, prefix):
    yield '[\''
    yield prefix
    yield '\',\''
    yield html_escape(structure.title.lower())
    yield '\','
    children = structure.children
    if children is None:
        yield 'null'
    else:
        yield '['
        for index, child in enumerate(children):
            yield from build_js_structure_gen(child, f'{prefix}_{index}')
        yield ']'
    
    yield '],'

SVG_PATH_CLOSED = '<path d="m 1 5 l 0 2 l 12 0 l 0 -2"></path>'
SVG_PATH_NONE = '<path d="M 3 6 a 3 3 0 1 1 6 0 a 3 3 0 1 1 -6 0"></path>'

def build_html_structure(structure):
    parts = []
    children = structure.children
    if (children is not None):
        parts.append('<ul>')
        
        for index, child in enumerate(children):
            parts.extend(build_html_structure_gen(child, f'ct_{index}'))
        
        parts.append('</ul>')
    
    return ''.join(parts)

def build_html_structure_gen(structure, prefix):
    yield '<li id="'
    yield prefix
    yield '">'
    
    children = structure.children
    yield '<svg id="'
    yield prefix
    yield '_s" onclick="ct.click(\''
    yield prefix
    yield '\');">'
    if children is None:
        yield SVG_PATH_NONE
    else:
        yield SVG_PATH_CLOSED
    yield '</svg>'
    
    yield '<a href="#'
    yield structure.prefixed_title
    yield '">'
    yield structure.title
    yield '</a>'
    
    if (children is not None):
        yield '<ul id="'
        yield prefix
        yield '_c" style="display: none;">'
        
        for index, child in enumerate(children):
            yield from build_html_structure_gen(child, f'{prefix}_{index}')
        
        yield '</ul>'
    
    yield '</li>'


