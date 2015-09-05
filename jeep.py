from entity import *
from renderable import *
from physical import *
import numpy as np
from input import *
import pygame
from math import *
from bullet import *

lines = np.array([[-10,5,1], [10,5,1], [10,-5,1], [-10,-5,1]])

class Jeep(Entity):
    def __init__(self, objects):
        super(Jeep, self).__init__(objects)
        physical = Physical()
        self.attach_component(physical)
        self.attach_component(Renderable(lines))
        inp = KeyboardController()
        def angle_to_direction(bag):
            speed = 5
            angle = pi * bag['angle']/180.
            bag['x'] += speed * cos(angle)
            bag['y'] += speed * sin(angle)
            return bag
        inp.bind_key(pygame.K_UP, self.modify_bag(angle_to_direction))
        #inp.bind_key(pygame.K_DOWN, lambda self: self.modify_bag('y', lambda y: y+1))
        turning_speed = 2
        inp.bind_key(pygame.K_LEFT,
                self.modify_bag_key('angle', lambda x: x-turning_speed))
        inp.bind_key(pygame.K_RIGHT,
                self.modify_bag_key('angle', lambda x: x+turning_speed))
        inp.bind_key(pygame.K_SPACE,
                lambda e: self.fire_bullet())
        self.attach_component(inp)

    def fire_bullet(self):
        bullet = Bullet(self.objects, self.bag)
        self.spawn_object(bullet)

