# main.py
# Aesthetics are managed here.

from tkinter import *
from ttkthemes import *
from turtle import *

import gravity

root = ThemedTk() # The actual window that'll pop up when you start the program.
root.title("Seitan!")
root.resizable(False,False)

root_canvas = Canvas(root,height=500,width=500, bg="#FFFFFF") # The "turtle" will draw onto this canvas here. It's black as indicated by the hex.
root_draw = RawTurtle(root_canvas) # This is the main drawing machinery.
root_draw.shape("turtle")

root_canvas.pack()

# Start up the main window

root.mainloop()