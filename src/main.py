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

delta_t = 86400/4
a = 0
b = 86400 * 10 * 365

universe = gravity.Universe(radius=150)

p1 = gravity.Particle(universe,root_canvas,[-10,10],[10e-7,10e-7],100)
p2 = gravity.Particle(universe,root_canvas,[0,0],[10e-7,10e-8],200)
p3 = gravity.Particle(universe,root_canvas,[10,10],[0,-10e-8],300)

universe.startSimulation(a,b,delta_t)
# Start up the main window


root.mainloop()