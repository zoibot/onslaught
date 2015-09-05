from component import *
import pygame

class KeyboardController(Component):
    keydowncodes = {}
    keycodes = {}
    keysdown = {}

    def bind_key(self, key, fn):
        self.keycodes[key] = fn

    def bind_key_down(self, key, fn):
        self.keydowncodes[key] = fn

    def update(self, entity):
        pressed = pygame.key.get_pressed()
        for key in self.keycodes:
            if pressed[key]:
                self.keycodes[key](entity)
        for key in self.keydowncodes:
            if pressed[key]:
                if not self.keysdown[key]:
                    self.keydowncodes[key](entity)
            self.keysdown[key] = pressed[key]
