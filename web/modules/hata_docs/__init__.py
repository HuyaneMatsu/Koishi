# -*- coding: utf-8 -*-
import sys
import hata
import hata.ext.patchouli
import hata.ext.extension_loader
import hata.ext.commands

from hata.ext.patchouli import map_module, MAPPED_OBJECTS
map_module('hata')

from flask import Blueprint

ROUTES = Blueprint('docs', 'hata_docs', url_prefix='/docs')

class DocsWrapper(object):
    __slots__ = ('path', 'unit',)
    
    @property
    def __name__(self):
        return self.path
    
    def __init__(self, path, unit):
        self.path = path
        self.unit = unit
    
    def __call__(self):
        return self.unit.name

path = unit = None

for path, unit in MAPPED_OBJECTS.items():
    path = '/'+'/'.join(path.parts)
    ROUTES.route(path)(DocsWrapper(path, unit))

del path, unit
