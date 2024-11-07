from math import *
from turtle import *

G = 6.67*10**(-10)# This is the universal gravitational constant (https://en.wikipedia.org/wiki/Gravitational_constant) if we were to put the real value the simulation wouldn't quite work due to rounding error.
SOFTENING_CONSTANT = 10# When particles get too close to one another, their acceleration may shoot into infinity. This softening constant is added to prevent that.
BODY_LIMIT = 10 # Upper bound to particles that can be generated.

def vectorMagnitude(v): 
    # Vector magnitude in R2
    return sqrt(v[0]**2+v[1]**2)

class Universe:
    def __init__(self,radius):
        self.children = []
        self.radius = radius
        self.isRunning = False
    def getChildren(self):
        return self.children
    def addChild(self,particle):
        self.children.append(particle)
    def startSimulation(self,a,b,delta_t):
        if self.isRunning == True:
            print("Simulation is already running! Please stop the simulation before running this command again!")
            return
        self.isRunning = True
        while self.isRunning == True:
            while a < b:
                for particle in self.getChildren():
                    particle.calculatePosition(delta_t)
                a += delta_t
            self.isRunning = False
    def stop(self):
        self.isRunning = False

class Particle:
    # THIS is where our particles are initialized.
    # It follows that each particle is given a position vector in R^2 and an acceleration vector in R^2.
    
    def __init__(self, parent, canvas, position=[0,0], velocity=[0,0],mass=1):
        self.position = position
        self.velocity = velocity
        self.acceleration = [0,0]
        self.netForce = [0,0]
        self.mass = mass
        
        self.scaling_factor = (parent.radius/10**2.5)
        self.turtle = RawTurtle(canvas)
        self.turtle.shape("circle")
        self.turtle.penup()
        self.turtle.goto(self.position[0]/self.scaling_factor,self.position[1]/self.scaling_factor)
        
        self.parent = parent
        self.parent.addChild(self)
        
        
    def calculatePosition(self,delta_t):
        F_x = 0
        F_y = 0
        for particle in self.parent.getChildren():
            if particle != self: ## Don't calculate the force exerted on a particle by itself!
                delta_x = particle.position[0]-self.position[0]
                delta_y = particle.position[1]-self.position[1]
                F = G*self.mass*particle.mass/(delta_x**2+delta_y**2)
                F_x += F*delta_x/sqrt(delta_x**2 + delta_y**2)
                F_y += F*delta_y/sqrt(delta_x**2+delta_y**2)
                #print(F_x,F_y)
                #print("###")
        self.netForce = [F_x,F_y]
        a_x = self.netForce[0]/self.mass
        a_y = self.netForce[1]/self.mass
        self.acceleration = [a_x,a_y]
        self.velocity = [self.velocity[0]+delta_t*self.acceleration[0],self.velocity[1]+delta_t*self.acceleration[1]]
        self.position = [self.position[0] + delta_t*self.velocity[0],self.position[1] + delta_t*self.velocity[1]]
        self.turtle.goto(self.position[0]/self.scaling_factor,self.position[1]/self.scaling_factor)
    
