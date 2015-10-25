import numpy as np

from entity import *
from physical import *
from renderable import *
from math import *
from destroyable import *

lines = np.array([[-10,0,1], [10,0,1]])

class Bullet(Entity):
    def __init__(self, objects, bag):
        super(Bullet, self).__init__(objects)
        self.attach_component(Physical())
        self.attach_component(Renderable(lines))
        print bag
        self.bag['x'] = bag['x']
        self.bag['y'] = bag['y']
        self.bag['angle'] = bag['angle']

    def update(self):
        super(Bullet, self).update()
        speed = 5
        angle = pi * self.bag['angle']/180.
        self.bag['x'] += speed * cos(angle)
        self.bag['y'] += speed * sin(angle)
        x, y = self.bag['x'], self.bag['y']
        if (x < 0 or 640 < x) or (y < 0 or 480 < y): 
            self.destroy()
        for destroyable in get_destroyables():
            if destroyable.collides(x, y):
                destroyable.destroy()
                self.destroy()
    

