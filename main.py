import sys
import pygame
import gfx

from jeep import Jeep
from tank import Tank

objects = []
objects_to_add = []
jeep = Jeep(objects_to_add)

def spawn_tank():
    tank = Tank(objects_to_add)
    tank.bag['tankx'] = 100
    tank.bag['tanky'] = 100
    tank.bag['barrelx'] = 100
    tank.bag['barrely'] = 100

waves = [10, 10000, 15000, 20000, 23000, 25000]

def main():
    global objects
    gfx.init()
    clock = pygame.time.Clock()
    frame = 0
    while True:
        frame += clock.get_time()
        if frame > waves[0]:
            waves.pop(0)
            spawn_tank()
            if not waves:
                print 'you win!'
                sys.exit(1)
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_q:
                    sys.exit(0)
        if objects_to_add:
            objects += objects_to_add
            del objects_to_add[:]
        for obj in objects:
            obj.update()
        # TODO clean this up
        new_objects = []
        for object in objects:
            if object.dead:
                for component in object.components:
                    component.detach(object)
            else:
                new_objects.append(object)
    
        objects = new_objects
        gfx.loop()
    
try:
    main()
finally:
    gfx.cleanup()

