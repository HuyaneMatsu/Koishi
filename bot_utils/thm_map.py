# -*- coding: utf-8 -*-
from collections import namedtuple

Cube = namedtuple('Cube', ['x', 'y', 'z'])
Axial = namedtuple('Axial', ['x', 'y'])

def get_ring_level(cube):
    x, y, z = cube
    
    if x < 0:
        x = -x
    
    max_ = x
    
    if y < 0:
        y = -y
    
    if y > max_:
        max_ = y
    
    if z < 0:
        z = -z
    
    if z > max_:
        max_ = z
    
    return max_

def get_passed_cells(ring_level):
    if ring_level == 0:
        return 0
    
    return 1+(((ring_level+1)*ring_level)*3)

def axial_to_cube(axial):
    x = axial.x
    y = axial.y
    
    return Cube(x, -x-y, y)

def cube_to_axial(cube):
    return  Axial(cube.x, cube.z)

def generate_map(size):
    map_ = []
    min_ = -size
    max_ = size+1
    for x in range(min_, max_):
        for y in range(min_, max_):
            for z in range(min_, max_):
                if x+y+z == 0:
                    map_.append(Cube(x, y, z))
    
    return map_

