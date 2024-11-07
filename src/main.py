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

root_canvas = Canvas(root,height=1000,width=1000, bg="#000000") # The "turtle" will draw onto this canvas here. It's black as indicated by the hex.

root_canvas.pack()
root_canvas.configure(bg="#000000")
# Commence the actual math & computation!

delta_t = 86400
a = 0
b = 86400 * 10 * 365

universe = gravity.Universe(radius=2.50e+11)

earth = gravity.Particle(universe,root_canvas,[1.4960e+11,0.0000e+00],[0.0000e+00,2.9800e+04],5.9740e+24,"Earth")
mars = gravity.Particle(universe,root_canvas,[2.2790e+11,0.0000e+00],[0.0000e+00, 2.8100e+04],6.4190e+23,"Mars")
mercury = gravity.Particle(universe,root_canvas,[5.7900e+10, 0.0000e+00],[0.0000e+00, 1.7900e+04],3.3020e+23,"Mercury")
sun = gravity.Particle(universe,root_canvas,[0.0000e+00,0.0000e+00],[0.0000e+00, 0.0000e+00],1.9890e+30,"Sun")
venus = gravity.Particle(universe,root_canvas,[1.0820e+11, 0.0000e+00],[0.0000e+00, -1.5000e+04],4.8690e+24,"Venus")

universe.startSimulation(a,b,delta_t,output=True)

# Start up the main window

root.mainloop()