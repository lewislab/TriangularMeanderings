#! /usr/bin/python


# Experimetnal parameters
# 800 micron nozzle @1.2mm width
# @0.7mm layer height
# 
from mecode import G
import numpy as np

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

g = G()
g.set_home(x=0,y=0,z=0)
for idx in range(len(heights)):
    g.absolute()
    g.feed(travel_feed)
    g.move(z=heights[idx])
    if idx % 2 == 0:
        if idx != 0:
            g.move(-5, x_width)
        g.move(0,0)
        g.move
        g.relative()
        g.triangular_meander(x_width,y_width,spacing,extrusion_width,travel_feed=travel_feed,print_feed=print_feed,start='LL')
    else:
        g.move(-5, -5)
        g.move(0 , y_width)
        g.relative()
        g.triangular_meander(x_width,y_width,spacing,extrusion_width,travel_feed=travel_feed,print_feed=print_feed,start='UR')

g.move(x=x_width+2,y=y_width+2, z=0) # move over and go back to zero


g.view(backend="matplotlib")
g.teardown()
