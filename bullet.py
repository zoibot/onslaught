import numpy as np

from entity import *
from physical import *
from renderable import *

lines = np.array([[-10,0,1], [10,0,1]])

class Bullet(Entity):
    def __init__(self, objects, bag):
        super(Bullet, self).__init__(objects)
        self.attach_component(Physical())
        self.attach_component(Renderable(lines))
        self.bag['x'] = bag['x']
        self.bag['y'] = bag['y']
        self.bag['angle'] = bag['angle']

