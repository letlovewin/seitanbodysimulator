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

universe = gravity.Universe(radius=150)

for i in range(4):
    px = random.uniform(-150/2,150/2)
    py = random.uniform(-150/2,150/2)
    vx = random.uniform(-10e-6,10e-6)
    vy = random.uniform(-10e-6,10e-6)
    mass = random.uniform(50,250)
    particle = gravity.Particle(universe,root_canvas,[px,py],[vx,vy],mass)

universe.startSimulation(a,b,delta_t)

root.mainloop()