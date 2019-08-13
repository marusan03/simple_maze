"""This is a test program."""

import sys

import pygame
from pygame.locals import (
    QUIT,
    KEYDOWN,
    K_ESCAPE,
    K_LEFT,
    K_RIGHT,
    K_UP,
    K_DOWN,
    K_SPACE)

# from config import Config
from maze import build_maze
from player import Player
from goal import Goal
from utils import Directions, screenshot

pygame.init()


def main(scale):
    """main loop"""
    SURFACE = pygame.display.set_mode((160*4, 160*4))
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('simple maze')
    maze, accesible_map = build_maze(scale, scale)
    player = Player(scale, accesible_map)
    goal = Goal(scale)

    SURFACE.fill([255, 0, 255])

    maze_surface = maze.copy()
    backgrand = maze.copy()
    SURFACE.blit(pygame.transform.scale(
        maze, [160*4, 160*4]), [0, 0])

    sprites = pygame.sprite.LayeredDirty(
        player, goal)

    directions = Directions()

    while True:

        sprites.clear(maze_surface, backgrand)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                # ESCキーなら終了
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                # 矢印キーなら円の中心座標を矢印の方向に移動
                if event.key == K_LEFT:
                    player.update(
                        directions.direction_to_flag(directions.left))
                if event.key == K_RIGHT:
                    player.update(
                        directions.direction_to_flag(directions.right))
                if event.key == K_UP:
                    player.update(
                        directions.direction_to_flag(directions.up))
                if event.key == K_DOWN:
                    player.update(
                        directions.direction_to_flag(directions.down))
                if event.key == K_SPACE:
                    screen = pygame.transform.scale(
                        maze_surface, [160*4, 160*4])
                    screenshot(pygame.surfarray.array3d(screen).swapaxes(0, 1))

        if pygame.sprite.collide_rect(player, goal):
            player.reset()
            goal.reset()

        dirty_rects = sprites.draw(maze_surface)

        SURFACE.blit(pygame.transform.scale(
            maze_surface, [160*4, 160*4]), [0, 0])

        pygame.display.update(dirty_rects)
        print(f'fps:{int(1/((FPSCLOCK.tick()/1000)+10e-4))}\r', end='')


if __name__ == '__main__':
    main(scale=3)
