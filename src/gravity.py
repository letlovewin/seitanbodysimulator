# Written by GRAY
# Yes, I'm aware this code is extremely messy and hacky. It'll be fixed at some point in the near future.

from math import *
from turtle import *

G = 6.67*10**(-11)# This is the universal gravitational constant (https://en.wikipedia.org/wiki/Gravitational_constant) if we were to put the real value the simulation wouldn't quite work due to rounding error.
SOFTENING_CONSTANT = 10# When particles get too close to one another, their acceleration may shoot into infinity. This softening constant is added to prevent that.
BODY_LIMIT = 10 # Upper bound to particles that can be generated.
THETA = 0.5

def is_in(x_p,y_p,x_interval,y_interval):
    if x_p >= x_interval[0] and x_p <= x_interval[1] and y_p >= y_interval[0] and y_p <= y_interval[1]:
        return True
    return False

class Quadrant:
    def __init__(self,x,y,length):
        self.x = x
        self.y = y
        self.length = length
    def length(self):
        return self.length
    def contains(self,particle):
        return is_in(particle.position[0],particle.position[1],[self.x,self.x+self.length],[self.y,self.y+self.length])
    def NW(self):
        return Quadrant(self.x,self.y+self.length/2,self.length/2)
    def NE(self):
        return Quadrant(self.x+self.length/2,self.y+self.length/2,self.length/2)
    def SW(self):
        return Quadrant(self.x,self.y,self.length/2)
    def SE(self):
        return Quadrant(self.x+self.length/2,self.y,self.length/2)
    
class BarnesHutTree:
    def __init__(self,quadrant,particle=None):
        self.body = particle
        self.children = [None,None,None,None]
        # For the children, 0 is northeast, 1 is northwest, 2 is southwest, 3 is southeast.
        self.COM = [0,0]
        self.mass = 0
        self.quadrant = quadrant
    def isEmpty(self):
        if self.children == [None,None,None,None]:
            return True
        return False
    def getQuadrant(self):
        return self.quadrant
    def getNorthEast(self):
        return self.children[0]
    def getNorthWest(self):
        return self.children[1]
    def getSouthWest(self):
        return self.children[2]
    def getSouthEast(self):
        return self.children[3]
    def getTotalMass(self,mass=0):
        if self.isEmpty() and self.body:
            return self.body.mass
        if self.isEmpty() and self.body == None:
            return 0
        temp = 0
        for tree in self.children:
            if tree:
                temp += tree.getTotalMass(mass)
        return mass + temp
    def getYMoment(self,yMoment=0):
        if self.isEmpty() and self.body:
            return self.body.position[1]*self.body.mass
        if self.isEmpty() and self.body == None:
            return 0
        temp = 0
        for tree in self.children:
            if tree:
                temp += tree.getYMoment(yMoment)
        return yMoment + temp
    def getXMoment(self,xMoment=0):
        if self.isEmpty() and self.body:
            return self.body.position[0]*self.body.mass
        if self.isEmpty() and self.body == None:
            return 0
        temp = 0
        for tree in self.children:
            if tree:
                temp += tree.getXMoment(xMoment)
        return xMoment + temp
        
    def traverse(self):
        if self.isEmpty():
            if self.body != None:
                print(self.body.mass)
            return
        for child in self.children:
            child.traverse()
    def getCOM(self):
        xMoment = self.getXMoment()
        yMoment = self.getYMoment()
        totalMass = self.getTotalMass()
        return [yMoment/totalMass,xMoment/totalMass]
    def insert(self,particle):
        if self.body == None and self.isEmpty():
            self.body = particle
            return
        if self.isEmpty():
            nw = self.quadrant.NW()
            ne = self.quadrant.NE()
            sw = self.quadrant.SW()
            se = self.quadrant.SE()
            
            if nw.contains(particle):
                if self.children[0] == None:
                    self.children[0] = BarnesHutTree(nw)
                self.children[0].insert(particle)
            elif ne.contains(particle):
                if self.children[1] == None:
                    self.children[1] = BarnesHutTree(ne)
                self.children[1].insert(particle)
            elif sw.contains(particle):
                if self.children[2] == None:
                    self.children[2] = BarnesHutTree(sw)
                self.children[2].insert(particle)
            elif se.contains(particle):
                if self.children[3] == None:
                    self.children[3] = BarnesHutTree(se)
                self.children[3].insert(particle)
            
            if nw.contains(self.body):
                if self.children[0] == None:
                    self.children[0] = BarnesHutTree(nw)
                self.children[0].insert(self.body)
            elif ne.contains(self.body):
                if self.children[1] == None:
                    self.children[1] = BarnesHutTree(ne)
                self.children[1].insert(self.body)
            elif sw.contains(self.body):
                if self.children[2] == None:
                    self.children[2] = BarnesHutTree(sw)
                self.children[2].insert(self.body)
            elif se.contains(self.body):
                if self.children[3] == None:
                    self.children[3] = BarnesHutTree(se)
                self.children[3].insert(self.body)
                
            self.body = None
            return
        for tree in self.children:
            if tree:
                if tree.quadrant.contains(particle):
                    tree.insert(particle)
                    return
        return
    def updateForce(self,particle,nF_x=0,nF_y=0):
        if self.isEmpty() and self.body:
            if self.body == particle:
                return [0,0]
            delta_x = self.body.position[0]-particle.position[0]
            delta_y = self.body.position[1]-particle.position[1]
            r = sqrt(delta_x**2 + delta_y**2)
            F = G*self.body.mass*particle.mass/(r**2+SOFTENING_CONSTANT**2)
            return [F*delta_x/r,F*delta_y/r]
        if self.isEmpty() and self.body == None:
            return [0,0]
        com = self.getCOM()
        s = self.quadrant.length
        delta_x = com[0]-particle.position[0]
        delta_y = com[1]-particle.position[1]
        d = sqrt(delta_x**2+delta_y**2)
        if s/d < THETA:
            total_mass = self.getTotalMass()
            r = sqrt(delta_x**2 + delta_y**2)
            F = G*total_mass*particle.mass/(r**2+SOFTENING_CONSTANT**2)
            return [F*delta_x/r,F*delta_y/r]
        else:
            totalForce_x = 0
            totalForce_y = 0
            for tree in self.children:
                if tree:
                    tf = tree.updateForce(particle,nF_x,nF_y)
                    totalForce_x += tf[0]
                    totalForce_y += tf[1]
            #neF = self.children[0].updateForce(particle,nF_x,nF_y)
            #nwF = self.children[1].updateForce(particle,nF_x,nF_y)
            #swF = self.children[2].updateForce(particle,nF_x,nF_y)
            #seF = self.children[3].updateForce(particle,nF_x,nF_y)
            #return [neF[0]+nwF[0]+swF[0]+seF[0],neF[1]+nwF[1]+swF[1]+seF[1]]
            return [totalForce_x,totalForce_y]

class Universe:
    def __init__(self,radius):
        self.children = []
        self.radius = radius
        self.isRunning = False
    def getChildren(self):
        return self.children
    def addChild(self,particle):
        self.children.append(particle)
    def startSimulation(self,a,b,delta_t,output=False):
        if self.isRunning == True:
            print("Simulation is already running! Please stop the simulation before running this command again!")
            return
        self.isRunning = True
        while self.isRunning == True:
            while a < b:
                bht = BarnesHutTree(Quadrant(0,0,self.radius))
                for particle in self.getChildren():
                    bht.insert(particle)
                for particle in self.getChildren():
                    F_xy = bht.updateForce(particle)
                    a_x = F_xy[0]/particle.mass
                    a_y = F_xy[1]/particle.mass
                    particle.acceleration = [a_x,a_y]
                    particle.velocity = [particle.velocity[0]+delta_t*particle.acceleration[0],particle.velocity[1]+delta_t*particle.acceleration[1]]
                    particle.position = [particle.position[0] + delta_t*particle.velocity[0],particle.position[1] + delta_t*particle.velocity[1]]
                    particle.turtle.goto(particle.position[0]/particle.scaling_factor,particle.position[1]/particle.scaling_factor)
                a += delta_t
            self.isRunning = False
        if output == True:
            for particle in self.getChildren():
                print(particle.name)
                print("Position: ", particle.position)
                print("Velocity: ", particle.velocity)
                print("Mass: ", particle.mass)
    def startSimulationNaive(self,a,b,delta_t,output=False):
        if self.isRunning == True:
            print("Simulation is already running! Please stop the simulation before running this command again!")
            return
        self.isRunning = True
        while self.isRunning == True:
            while a < b:
                for particle in self.getChildren():
                    for other in self.getChildren():
                        if particle != other:
                            delta_x = particle.position[0]-other.position[0]
                            delta_y = particle.position[1]-other.position[1]
                            r = sqrt(delta_x**2 + delta_y**2)
                            F = G*particle.mass*other.mass/(r**2+SOFTENING_CONSTANT**2)
                            F_x = F*delta_x/r
                            F_y = F*delta_y/r
                            a_x = F_x/particle.mass
                            a_y = F_y/particle.mass
                            particle.acceleration = [a_x,a_y]
                            particle.velocity = [particle.velocity[0]+delta_t*particle.acceleration[0],particle.velocity[1]+delta_t*particle.acceleration[1]]
                            particle.position = [particle.position[0] + delta_t*particle.velocity[0],particle.position[1] + delta_t*particle.velocity[1]]
                            particle.turtle.goto(particle.position[0]/particle.scaling_factor,particle.position[1]/particle.scaling_factor)
                a += delta_t
            self.isRunning = False
        if output == True:
            for particle in self.getChildren():
                print(particle.name)
                print("Position: ", particle.position)
                print("Velocity: ", particle.velocity)
                print("Mass: ", particle.mass)
    def stop(self):
        self.isRunning = False

class Particle:
    # THIS is where our particles are initialized.
    # It follows that each particle is given a position vector in R^2 and an acceleration vector in R^2.
    
    def __init__(self, parent, canvas, position=[0,0], velocity=[0,0],mass=1,name="Particle"):
        self.position = position
        self.velocity = velocity
        self.acceleration = [0,0]
        self.netForce = [0,0]
        self.mass = mass
        self.name = name
        
        self.scaling_factor = (parent.radius/10**2.6)
        self.turtle = RawTurtle(canvas)
        
        self.canvas = canvas
        self.turtle.shape("circle")
        self.turtle.penup()
        self.turtle.goto(self.position[0]/self.scaling_factor,self.position[1]/self.scaling_factor)
        
        self.parent = parent
        self.parent.addChild(self)
        
    def is_in(self,quadrant):
        return quadrant.contains(self)
    
    def add(self,p1,p2):
        m = p1.mass + p2.mass
        COM_particle = Particle(self.parent,self.canvas,)
        
    def calculatePosition(self,delta_t):
        # A naive implementation of gravitational force calculation.
        # https://www.cs.princeton.edu/courses/archive/spr15/cos126/assignments/nbody.html
        F_x = 0
        F_y = 0
        for particle in self.parent.getChildren():
            if particle != self: ## Don't calculate the force exerted on a particle by itself!
                delta_x = particle.position[0]-self.position[0]
                delta_y = particle.position[1]-self.position[1]
                r = sqrt(delta_x**2 + delta_y**2) # r is the distance from body 1 to body 2
                F = G*self.mass*particle.mass/(r**2+SOFTENING_CONSTANT**2)
                F_x += F*delta_x/r
                F_y += F*delta_y/r
        self.netForce = [F_x,F_y]
        a_x = self.netForce[0]/self.mass
        a_y = self.netForce[1]/self.mass
        self.acceleration = [a_x,a_y]
        self.velocity = [self.velocity[0]+delta_t*self.acceleration[0],self.velocity[1]+delta_t*self.acceleration[1]]
        self.position = [self.position[0] + delta_t*self.velocity[0],self.position[1] + delta_t*self.velocity[1]]
        self.turtle.goto(self.position[0]/self.scaling_factor,self.position[1]/self.scaling_factor)
    
