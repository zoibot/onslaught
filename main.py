import sys
import pygame
import gfx
import object_manager
import game_state

from jeep import Jeep
from tank import Tank

objects = []
objects_to_add = []
jeep = Jeep(objects_to_add)
jeep.bag['x'] = 200
jeep.bag['y'] = 200

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
    object_manager.init(objects)
    clock = pygame.time.Clock()
    ticks = 0
    score_text = gfx.create_text()
    gfx.show_text(score_text, True)
    gfx.set_text_transform(score_text, [320, 20], 0)
    while True:
        clock.tick(60)
        ticks += clock.get_time()
        gfx.set_text(score_text, game_state.get_score())
        if ticks > waves[0] and len(object_manager.find_objects(Tank)) == 0:
            waves.pop(0)
            spawn_tank()
            if not waves:
                # need to actually kill tanks
                print('you win!')
                sys.exit(1)
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

