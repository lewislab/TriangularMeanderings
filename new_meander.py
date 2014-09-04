#! /usr/bin/env python

from mecode import G
import numpy as np
import math
g = G()

box_x = 10
box_y = 10
spacing = 1
meander_start = 'LR'

def triangular_meander(g, x, y, spacing, start='LR'):
    # Calculate meander
    spacing = g.meander_spacing(box_y,spacing)
    passes = g.meander_passes(box_y, spacing)

    # Calculate tri wave
    tri_x_half_cycle = spacing/math.sqrt(3)
    tri_y_half_cycle = spacing

    cycles = box_x/(tri_x_half_cycle*2)

    if round(cycles) <= cycles: # if we round down
        cycles = round(cycles) + 0.5
    elif round(cycles) >= cycles: # if we round up
        cycles = round(cycles) - 0.5

    # Do meander
    g.meander(cycles*tri_x_half_cycle*2, box_y, spacing, start=meander_start)

    tri_wave_start = meander_start
    if passes%2==1.0:
        if meander_start[1] == 'R':
            tri_wave_start = tri_wave_start[0]+'L'
        elif meander_start[1] == 'L':
            tri_wave_start = tri_wave_start[0]+'R'

    for i in range(int(passes)):
        g.triangular_wave(tri_x_half_cycle, tri_y_half_cycle, cycles, start=tri_wave_start)
        if tri_wave_start[1] == 'R':
            tri_wave_start = tri_wave_start[0]+'L'
        elif tri_wave_start[1] == 'L':
            tri_wave_start = tri_wave_start[0]+'R'


start_height = 0
layer_count = 10
layer_thick = 0.2

heights = np.arange(start_height, layer_count*layer_thick, layer_thick)
g.absolute()
for height in heights:
    g.move(x=0, y=0, z=height)
    triangular_meander(g, box_x, box_y, spacing, start=meander_start)





g.view(backend="matplotlib")
