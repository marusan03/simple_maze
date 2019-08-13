import math
import pygame
import numpy as np
from .utils import Directions


class Player(pygame.sprite.DirtySprite):
    def __init__(self, scale, accesible_map):
        super().__init__()
        self.scale = scale
        self.color = (0, 144, 255)
        self.scale = scale

        self.image = pygame.Surface((1, 1))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (1, 1)
        self.topleft_map = np.array([1, 1])
        self.accesible_map = accesible_map

        self.directions = Directions()

    def update(self, flag):
        x, y = self.topleft_map
        if self.accesible_map[x][y] & flag:
            self.topleft_map += np.array(
                self.directions.flag_to_direction(flag))
            self.rect.topleft = self.topleft_map
            self.dirty = 1

    def reset(self):
        self.rect.topleft = (1, 1)
        self.topleft_map = np.array([1, 1])
