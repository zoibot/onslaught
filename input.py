from component import *
import pygame

class KeyboardController(Component):
    keycodes = {}

    def bind_key(self, key, fn):
        self.keycodes[key] = fn

    def update(self, entity):
        pressed = pygame.key.get_pressed()
        for key in self.keycodes:
            if pressed[key]:
                self.keycodes[key](entity)

