import numpy as np

from entity import *
from physical import *
from renderable import *
from destroyable import *
from math import *

tank_lines = np.array([[-15,8,1], [15,8,1], [15,-8,1], [-15,-8,1]])
barrel_lines = np.array([[-5,3,1], [20,3,1], [20,-3,1], [-5,-3,1]])

class Tank(Entity):
    def __init__(self, objects):
        super(Tank, self).__init__(objects)
        self.attach_component(Physical('tank'))
        self.attach_component(Physical('barrel'))
        self.attach_component(Renderable(tank_lines, 'tank'))
        self.attach_component(Renderable(barrel_lines, 'barrel'))
        self.attach_component(Destroyable(None, 'tank'))

    def update(self):
        self.bag['barrelangle'] += 2
        super(Tank, self).update()
        return
        speed = 5
        angle = pi * self.bag['angle']/180.
        self.bag['x'] += speed * cos(angle)
        self.bag['y'] += speed * sin(angle)
        #TODO kill bullets off screen
    

