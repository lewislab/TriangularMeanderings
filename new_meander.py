#! /usr/bin/env python

from mecode import G
import numpy as np
import math
g = G()

box_x = 20
box_y = 20
walls = 3
spacing = 5
meander_start = 'LL'
extrusion_width = 0.2

nozzle = 0.2

start_height = 0
layer_count = 10
layer_thick = nozzle/2

def tri_meander_length(g, x, y, spacing, extrusion_width):
    # Calculate tri wave
    tri_x_length = x-extrusion_width
    tri_y_half_cycle = g.meander_spacing(y,spacing)-extrusion_width*2
    tri_x_half_cycle = (tri_y_half_cycle/math.sqrt(3))
    cycles = tri_x_length/(tri_x_half_cycle*2)

    if round(cycles) <= cycles: # if we round down
        cycles = round(cycles) + 0.5
    elif round(cycles) >= cycles: # if we round up
        cycles = round(cycles) - 0.5

    return cycles*tri_x_half_cycle*2+extrusion_width*2


def triangular_meander(g, x, y, spacing, start='LR', extrusion_width=0.0):
    # Calculate meander
    spacing = g.meander_spacing(y,spacing)
    passes = g.meander_passes(y, spacing)

    # Calculate tri wave
    tri_x_length = x-extrusion_width
    tri_y_half_cycle = spacing-extrusion_width*2
    tri_x_half_cycle = (tri_y_half_cycle/math.sqrt(3))

    cycles = tri_x_length/(tri_x_half_cycle*2)

    if round(cycles) <= cycles: # if we round down
        cycles = round(cycles) + 0.5
    elif round(cycles) >= cycles: # if we round up
        cycles = round(cycles) - 0.5

    new_box_x = cycles*tri_x_half_cycle*2+extrusion_width*2
    # Do meander
    g.meander(new_box_x, y, spacing, start=meander_start)

    tri_wave_start = meander_start
    if passes%2==1.0:
        if meander_start[1] == 'R':
            tri_wave_start = tri_wave_start[0]+'L'
        elif meander_start[1] == 'L':
            tri_wave_start = tri_wave_start[0]+'R'

    g.relative() #TODO: Return to origin axis mode
    if tri_wave_start == 'LL':
        g.move(x=-extrusion_width, y=-extrusion_width)
    elif tri_wave_start == 'LR':
        g.move(x=extrusion_width, y=-extrusion_width)
    elif tri_wave_start == 'UL':
        g.move(x=-extrusion_width, y=extrusion_width)
    elif tri_wave_start == 'UR':
        g.move(x=extrusion_width, y=extrusion_width)

    for i in range(int(passes)):
        g.triangular_wave(tri_x_half_cycle, tri_y_half_cycle, cycles, start=tri_wave_start)

        # cross over meander
        if tri_wave_start[0] == 'U':
            g.move(x=0, y=extrusion_width*2)
        elif tri_wave_start[0] == 'L':
            g.move(x=0, y=-extrusion_width*2)

        # alternate direction
        if tri_wave_start[1] == 'R':
            tri_wave_start = tri_wave_start[0]+'L'
        elif tri_wave_start[1] == 'L':
            tri_wave_start = tri_wave_start[0]+'R'


heights = np.arange(start_height, layer_count*layer_thick, layer_thick)

tri_length = tri_meander_length(g, box_x, box_y, spacing, extrusion_width)
for height in heights:
    for i in range(walls, 0, -1):
        g.absolute()
        g.move(x=-extrusion_width*i, y=-extrusion_width*i, z=height)
        g.relative()
        g.rect(tri_length+extrusion_width*i*2, box_y+extrusion_width*i*2)

    g.absolute()
    g.move(0,0)
    triangular_meander(g, box_x, box_y, spacing, start=meander_start, extrusion_width=extrusion_width)





g.view(backend="matplotlib")
