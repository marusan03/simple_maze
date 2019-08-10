import gym
import gym.spaces
import numpy as np

import pygame

# from config import Config
from .maze import build_maze
from .player import Player
from .goal import Goal
from .utils import Directions


class MuzeEnv(gym.Env):
    def __init__(self, **kwargs):
        super().__init__()
        pygame.init()
        self._shape = (160, 160, 3)
        self.observation_space = gym.spaces.Box(
            low=0,
            high=255,
            shape=self._shape,
            dtype=np.uint8
        )
        self.reward_range = [-1.0, 100.0]

        self.scale = 7
        self.surface = None
        self.dirty_rects = None
        self.action_space = gym.spaces.Discrete(4)
        self.maze, self.accesible_map = build_maze(self.scale, self.scale)

        self.maze_surface = self.maze.copy()
        self.backgrand = self.maze.copy()

        self.player = Player(self.scale, self.accesible_map)
        self.goal = Goal(self.scale)
        self.sprites = pygame.sprite.LayeredDirty(
            self.player, self.goal)

        self.directions = Directions()

    def reset(self):
        self.player.reset()
        self.goal.reset()
        self.maze_surface = self.maze.copy()
        self.backgrand = self.maze.copy()

        self.dirty_rects = self.sprites.draw(self.maze_surface)
        screen = pygame.transform.scale(self.maze_surface, [160, 160])
        observation = pygame.surfarray.array3d(screen).swapaxes(0, 1)

        screen = pygame.transform.scale(
            self.maze_surface, [160*4, 160*4])

        return observation

    def step(self, action):
        pygame.event.pump()
        info = False
        self.sprites.clear(self.maze_surface, self.backgrand)
        self.player.update(1 << action)
        if pygame.sprite.collide_rect(self.player, self.goal):
            reward = 100
            done = True
        else:
            reward = -1
            done = False
        self.dirty_rects = self.sprites.draw(self.maze_surface)
        screen = pygame.transform.scale(self.maze_surface, [160, 160])
        observation = pygame.surfarray.array3d(screen).swapaxes(0, 1)

        return observation, reward, done, info

    def render(self):
        if self.surface is None:
            self.surface = pygame.display.set_mode((160*4, 160*4))
            pygame.display.set_caption('maze')
            self.clock = pygame.time.Clock()
            self.surface.blit(pygame.transform.scale(
                self.maze, [160*4, 160*4]), [0, 0])

        self.surface.blit(pygame.transform.scale(
            self.maze_surface, [160*4, 160*4]), [0, 0])
        pygame.display.update(self.dirty_rects)
        print(f'fps:{int(1/((self.clock.tick(60)/1000)+10e-4))}\r', end='')

    def close(self):
        pass

    def seed(self, seed=None):
        pass
