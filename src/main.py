# main.py
# Aesthetics are managed here.

from tkinter import *
from ttkthemes import *
from turtle import *

import gravity
import random
import time

root = ThemedTk() # The actual window that'll pop up when you start the program.
root.title("Seitan N-Body Simulator")
root.resizable(False,False)

root_canvas = Canvas(root,height=1000,width=1000) # The "turtle" will draw onto this canvas here. It's black as indicated by the hex.

root_canvas.pack()

# Commence the actual math & computation!

delta_t = 86400
a = 0
b = 86400 * 10 * 365

universe = gravity.Universe(radius=1000)

p1 = gravity.Particle(universe,root_canvas,[100,100],[0,0],300)
p2 = gravity.Particle(universe,root_canvas,[510,510],[0,0],100)
p3 = gravity.Particle(universe,root_canvas,[200,200],[0,0],350)

#universe.startSimulation(a,b,delta_t,output=True)
q = gravity.Quadrant(0,0,1000)
b = gravity.BarnesHutTree(q)
b.insert(p1)
b.insert(p2)
b.insert(p3)

b.traverse()
print(b.getCOM())
print(b.updateForce(p1))
# Start up the main window


root.mainloop()