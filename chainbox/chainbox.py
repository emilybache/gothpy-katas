##
## ChainBox game controller

import game
import gui

import time

g = game.ChainBox()
w = gui.ChainBox(g)
w.render(g)

for pos, p in [((2,3),1), ((3,4),2), ((2,2),1), ((4,3),2), ((3,2),1)]:
    g.place_marker(p, pos)
    w.render(g)
    time.sleep(1)

time.sleep(3)


