import sys
import pygame
import gfx

from jeep import *

objects = []
jeep = Jeep(objects)
while True:
    gfx.init()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gfx.cleanup()
            sys.exit(0)
        for obj in objects:
            obj.update()
        gfx.loop()

