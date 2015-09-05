import sys
import pygame
import gfx

from jeep import *

objects = []
objects_to_add = []
jeep = Jeep(objects_to_add)

gfx.init()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gfx.cleanup()
            sys.exit(0)
    if objects_to_add:
        objects += objects_to_add
        del objects_to_add[:]
        print objects
    for obj in objects:
        obj.update()
    gfx.loop()

