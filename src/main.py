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
root.resizable(True,True)

root_canvas = Canvas(root,height=1000,width=1000, bg="#000000") # The "turtle" will draw onto this canvas here. It's black as indicated by the h

universe = gravity.Universe(radius=150)

#Beginning of aesthetics

def on_button_click_start():
    root.mainloop() #! root.mainloop() or some sort of pause? Has inverted effect, will stop if clicked & otherway around
def on_button_click_stop():
    root.quit()

#Frame for left side UI elements
left_frame = Frame(root, width = 300, height = 200, bg = "#e5e2e2")
left_frame.pack(side = "left", fill="y")

#Buttons for start & stop of program
start_button = Button(left_frame, text= "Start Simulation",font=("Arial",14), borderwidth=5, relief="solid",padx=20,pady=10, command =on_button_click_start)
start_button.pack(fill="x")

stop_button = Button(left_frame,text="Stop Simultation",font=("Arial",14),borderwidth=5, relief="solid",padx=20,pady=10, command = on_button_click_stop)
stop_button.pack(fill="x")

#! Question of whether or not to create another particle class or import from gravity.py file?
#!  --- > See notes - savi

#Entry widgets for particle attributes
label_name = Label(left_frame, text = "Particle Name: ")
label_name.pack(fill="x")

entry_name = Entry(left_frame)
entry_name.pack(fill="x")

label_x = Label(left_frame, text = "X Position: ")
label_x.pack(fill="x")
entry_x = Entry(left_frame)
entry_x.pack(fill="x")

label_y = Label(left_frame, text = "Y Position: ")
label_y.pack(fill="x")
entry_y = Entry(left_frame)
entry_y.pack(fil ="x")

label_x_velocity = Label(left_frame, text = "X Velocity: ")
label_x_velocity.pack(fill="x")
entry_x_velocity = Entry(left_frame)
entry_x_velocity.pack(fill="x")

label_y_velocity = Label(left_frame, text = "Y Velocity: ")
label_y_velocity.pack(fill="x")
entry_y_velocity = Entry(left_frame)
entry_y_velocity.pack(fill="x")

label_mass = Label(left_frame, text = "Mass: ")
label_mass.pack(fill="x")
entry_mass = Entry(left_frame)
entry_mass.pack(fill="x")

button_create = Button(left_frame, text = "Add Particle", command=lambda : gravity.Particle(universe,root_canvas,[float(entry_x.get()),float(entry_y.get())],[float(entry_x_velocity.get(),entry_y_velocity.get())],entry_mass.get(),entry_name.get())) # ! Insert command here
button_create.pack(fill= "x")

root_canvas = Canvas(root,height=1000,width=1000) # The "turtle" will draw onto this canvas here. It's black as indicated by the hex.

root_canvas.pack()

# Commence the actual math & computation!

delta_t = 86400
a = 0
b = 86400 * 10 * 365



for i in range(4):
    px = random.uniform(-150,150)
    py = random.uniform(-150,150)
    vx = random.uniform(-10e-6,10e-6)
    vy = random.uniform(-10e-6,10e-6)
    mass = random.uniform(50,250)
    particle = gravity.Particle(universe,root_canvas,[px,py],[vx,vy],mass)

universe.startSimulation(a,b,delta_t)

root.mainloop()