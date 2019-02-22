"""This is a test program."""

import sys
import pygame
from pygame.locals import QUIT
import pyglet.window as pw

pygame.init()
SURFASCE = pygame.display.set_mode((210, 160))
pygame.display.set_caption('simple maze')


def main():
    """main loop"""
    while True:
        SURFASCE.fill((255, 255, 255))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()


if __name__ == '__main__':
    main()
