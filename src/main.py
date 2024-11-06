# main.py
# Aesthetics are managed here.

from tkinter import *
from ttkthemes import *
from turtle import *

import gravity
import random
import time

root = ThemedTk() # The actual window that'll pop up when you start the program.
root.title("Seitan!")
root.resizable(False,False)

root_canvas = Canvas(root,height=1000,width=1000, bg="#FFFFFF") # The "turtle" will draw onto this canvas here. It's black as indicated by the hex.

root_canvas.pack()

# Commence the actual math & computation!

delta_t = 1
a = 0
b = 10000000000

universe = gravity.Universe()



p1 = gravity.Particle(universe,root_canvas,[0,70],[.1,.2],10)
p1.turtle.pencolor("#E02F09")

p2 = gravity.Particle(universe,root_canvas,[-55,-25],[.1,.2],10)
p2.turtle.pencolor("#0993e0")

p3 = gravity.Particle(universe,root_canvas,[25,55],[-.1,-.1],100)

p4 = gravity.Particle(universe,root_canvas,[0,0],[0,0],10000)

while a < b:
    for particle in universe.getChildren():
        particle.calculatePosition(delta_t)
    a += delta_t

# Start up the main window

root.mainloop()