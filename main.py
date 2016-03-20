import sys
import pygame
import gfx
import object_manager
import game_state

from jeep import Jeep
from tank import Tank
from input import *

objects = []
objects_to_add = []

def spawn_jeep():
    jeep = Jeep(objects_to_add)
    jeep.bag['x'] = 200
    jeep.bag['y'] = 200
    return jeep

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
    inp = KeyboardController()

    clock = pygame.time.Clock()
    ticks = 0

    score_text = gfx.create_text()
    gfx.show_text(score_text, True)
    gfx.set_text_transform(score_text, [520, 20], 0)

    lives_text = gfx.create_text()
    gfx.show_text(lives_text, True)
    gfx.set_text_transform(lives_text, [20, 20], 0)

    inp.bind_key_down(pygame.K_o, lambda x: print(objects))

    jeep = None

    while True:
        clock.tick(60)
        ticks += clock.get_time()

        gfx.set_text(score_text, game_state.get_score())
        gfx.set_text(lives_text, game_state.get_lives())

        # todo rename from init because it's really update
        object_manager.init(objects)

        if not jeep or jeep.dead:
            jeep = spawn_jeep()

        if ticks > waves[0] and len(object_manager.find_objects(Tank)) == 0:
            waves.pop(0)
            spawn_tank()
            if not waves:
                # need to actually kill tanks
                print('you win!')
                sys.exit(0)

        # lol
        if int(game_state.get_lives()) < 0:
            print('you lose!')
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

