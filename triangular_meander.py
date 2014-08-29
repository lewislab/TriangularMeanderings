#! /usr/bin/python


# Experimetnal parameters
# 800 micron nozzle @1.2mm width
# @0.7mm layer height
# 
from mecode import G
import numpy as np
import math

height = 0.25
start_height = 0.0
end_height = 4.0
heights = np.arange(start_height, end_height+height, height)
travel_feed = 600
print_feed = 10
x_width = 50
y_width = 45
spacing = 11.25
extrusion_width = 1.0
borders = 3


# actual spacing
minor = y_width
major = x_width
passes = math.ceil(y_width / spacing)
actual_spacing = minor / passes
# calculate number of equilateral triangles, then adjust major axis
tri_height = abs(actual_spacing) - extrusion_width*2
tri_base = tri_height*2/math.sqrt(3)
tri_ct_unadj = (abs(major) - np.sign(major)*extrusion_width*2)/tri_base
tri_ct_adj = math.ceil(tri_ct_unadj) - 0.5 # end up on the next column
major_adj = (tri_ct_adj * tri_base) + extrusion_width*2
tri_ct_adj = abs(tri_ct_adj)


g = G()
g.set_home(x=0,y=0,z=0)
for idx in range(len(heights)):
    g.absolute()
    g.feed(travel_feed)
    g.move(z=heights[idx])
    if idx % 2 == 0: #start on LL
        g.move(x=-extrusion_width/np.sqrt(2)*(borders+0.0),y=-extrusion_width/np.sqrt(2)*(borders+0.0)) # move to border start
        for ct in range(borders, 0, -1):
            offset = extrusion_width/np.sqrt(2)
            g.relative()
            if ct != borders:
                g.move(x=offset, y=offset)
            x_rect = major_adj+extrusion_width*ct*2/np.sqrt(2)
            y_rect = y_width+extrusion_width*ct*2/np.sqrt(2)
            g.rect(x=x_rect, y=y_rect, start='LL')
            g.absolute()
        if idx != 0:
            g.move(-5, x_width)
        g.move(0,0)
        g.relative()
        g.triangular_meander(x_width,y_width,spacing,extrusion_width,travel_feed=travel_feed,print_feed=print_feed,start='LL')
    else: # start on UR
        g.move(x=-extrusion_width/np.sqrt(2)*(borders+0.0),y=-extrusion_width/np.sqrt(2)*(borders+0.0)) # move to border start
        for ct in range(borders, 0, -1):
            offset = extrusion_width/np.sqrt(2)
            g.relative()
            if ct != borders:
                g.move(x=offset, y=offset)
            x_rect = major_adj+extrusion_width*ct*2/np.sqrt(2)
            y_rect = y_width+extrusion_width*ct*2/np.sqrt(2)
            g.rect(x=x_rect, y=y_rect, start='LL')
            g.absolute()
        g.move(-5, -5)
        g.move(0 , y_width)
        g.relative()
        g.triangular_meander(x_width,y_width,spacing,extrusion_width,travel_feed=travel_feed,print_feed=print_feed,start='UR')

g.move(x=x_width+2,y=y_width+2, z=0) # move over and go back to zero


g.view(backend="matplotlib")
g.teardown()
