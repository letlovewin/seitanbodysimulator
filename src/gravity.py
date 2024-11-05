from sympy import * # The math library

class Particle:
    # THIS is where our particles are initialized.
    # It follows that each particle is given a position vector in R^2 and an acceleration vector in R^2.
    def __init__(self):
        self.position = ZeroMatrix(1,2)
        self.acceleration = ZeroMatrix(1,2)
    def update(self):
        pass


