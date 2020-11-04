# -*- coding: utf-8 -*-
from collections import namedtuple
from itertools import count
from PIL import Image as PIL
from math import sin, cos, pi

MAP_SIZE = 3
HEIGHT = 20
LINE_WIDTH = 5

STEP_LONG = sin(pi/3.0)
STEP_SHORT = cos(pi/3.0)
STEP_FULL = 1.0

SIZE_X = (STEP_LONG + ((2.0*STEP_LONG)*MAP_SIZE) + LINE_WIDTH)*2
SIZE_Y = (((STEP_SHORT+(STEP_FULL/2.0)) + (STEP_FULL+STEP_SHORT)*MAP_SIZE) * LINE_WIDTH)*2

HEX_SIZE_X = STEP_LONG*2.0
HEX_SIZE_Y = STEP_FULL+(2.0*STEP_SHORT)

HEX_SIZE_HALF_X = HEX_SIZE_X*0.5 + LINE_WIDTH
HEX_SIZE_HALF_Y = HEX_SIZE_Y*0.5 + LINE_WIDTH

Cube = namedtuple('Cube', ['x', 'y', 'z'])
Axial = namedtuple('Axial', ['x', 'y'])

def generate_map_coordinates():
    map_ = {}
    index = 0
    min_ = -MAP_SIZE
    max_ = MAP_SIZE+1
    for x in range(min_, max_):
        for y in range(min_, max_):
            for z in range(min_, max_):
                if x+y+z == 0:
                    map_[index] = Cube(x, y, z)
                    index += 1
    return map_

MAP = generate_map_coordinates()

def line_generator():
    line_lengths = []
    
    middle = (MAP_SIZE<<1)+1
    length = MAP_SIZE
    while True:
        length += 1
        if length == middle:
            break
        
        line_lengths.append(length)
        continue
    
    line_lengths.append(length)
    
    while True:
        length -= 1
        if length == MAP_SIZE:
            break
        
        line_lengths.append(length)
        continue
    
    lines = []
    
    bot_limit = float(LINE_WIDTH)
    
    for width in line_lengths:
        x_starting_shift = (SIZE_X-(width*2.0*STEP_LONG))*0.5
        top_limit = bot_limit
        bot_limit = bot_limit+STEP_SHORT
        
        x_shift = x_starting_shift
        
        for _ in range(width):
            line_start_x = x_shift
            x_shift += STEP_LONG
            line_end_x = x_shift
            
            lines.append((line_start_x, bot_limit, line_end_x, top_limit))
            
            line_start_x = x_shift
            x_shift += STEP_LONG
            line_end_x = x_shift
            
            lines.append((line_start_x, top_limit, line_end_x, bot_limit))
        
        top_limit = bot_limit
        bot_limit = bot_limit+STEP_FULL
        
        x_shift = x_starting_shift
        
        for _ in range(width+1):
            lines.append((x_shift, bot_limit, x_shift, top_limit))
            x_shift += STEP_LONG*2.0
            lines.append((x_shift, bot_limit, x_shift, top_limit))
        
        # CONTINUE
            
def generate_map_image(size):
    map_image = PIL.new('RGBA', (SIZE_X, SIZE_Y), (0, 0, 0, 0))
    
    # CONTINUE

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

