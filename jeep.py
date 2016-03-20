from input import *
import pygame
from bullet import *
from destroyable import Destroyable
import game_state

lines = np.array([[-10,5,1], [10,5,1], [10,-5,1], [-10,-5,1]])

class Jeep(Entity):
    def __init__(self, objects):
        super(Jeep, self).__init__(objects)
        physical = Physical()
        self.attach_component(physical)
        self.attach_component(Renderable(lines))
        self.attach_component(Destroyable())
        inp = KeyboardController()
        def angle_to_direction(bag):
            speed = 5
            angle = pi * bag['angle']/180.
            bag['x'] += speed * cos(angle)
            bag['y'] += speed * sin(angle)
            return bag
        inp.bind_key(pygame.K_UP, self.modify_bag(angle_to_direction))
        self.initialized = True
        turning_speed = 2
        inp.bind_key(pygame.K_LEFT,
                self.modify_bag_key('angle', lambda x: x-turning_speed))
        inp.bind_key(pygame.K_RIGHT,
                self.modify_bag_key('angle', lambda x: x+turning_speed))
        inp.bind_key_down(pygame.K_z,
                lambda e: self.fire_bullet())
        self.attach_component(inp)

    def destroy(self):
        game_state.lose_life()
        super(Jeep, self).destroy()

    def fire_bullet(self):
        Bullet(self.objects, type(self), self.bag)

