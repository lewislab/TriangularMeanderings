#! /usr/bin/python


# Experimetnal parameters
# 800 micron nozzle @1.2mm width
# @0.7mm layer height
# 
from mecode import G
import numpy as np

heights = [0.0, 0.7, 1.4, 2.1]
travel_feed = 600
print_feed = 10
x_width = 35
y_width = 30
spacing = 7.5
extrusion_width = 0.8

g = G()
g.set_home(x=0,y=0)
for idx in range(len(heights)):
    g.absolute()
    g.feed(travel_feed)
    g.move(Z=heights[idx])
    if idx % 2 == 0:
        g.move(-5, 35)
        g.move(0,0)
        g.move
        g.relative()
        g.triangular_meander(x_width,y_width,spacing,extrusion_width,travel_feed=travel_feed,print_feed=print_feed,start='LL')
    else:
        g.move(-5, -5)
        g.move(0 , 30)
        g.relative()
        g.triangular_meander(x_width,y_width,spacing,extrusion_width,travel_feed=travel_feed,print_feed=print_feed,start='UR')

g.teardown()
