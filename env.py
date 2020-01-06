import gym
import gym.spaces
import numpy as np

import pygame

# from config import Config
from .maze import build_maze
from .player import Player
from .goal import Goal
from .utils import Directions


class MazeEnv(gym.Env):
    def __init__(self, **kwargs):
        super().__init__()
        pygame.init()
        self._shape = (210, 160, 3)
        self.observation_space = gym.spaces.Box(
            low=0,
            high=255,
            shape=self._shape,
            dtype=np.uint8
        )
        self.reward_range = [-10.0, 10.0]

        self.scale = 5
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

        self.global_step = 0

    def reset(self):
        self.sprites.clear(self.maze_surface, self.backgrand)
        self.player.reset()
        self.goal.reset()
        # self.maze_surface = self.maze.copy()
        # self.backgrand = self.maze.copy()

        self.global_step = 0

        self.dirty_rects = self.sprites.draw(self.maze_surface)
        screen = pygame.transform.scale(self.maze_surface, [210, 160])
        observation = pygame.surfarray.array3d(screen).swapaxes(0, 1)

        screen = pygame.transform.scale(
            self.maze_surface, [160*4, 160*4])

        return observation

    def step(self, action):
        if not (self.surface is None):
            pygame.event.pump()
        self.sprites.clear(self.maze_surface, self.backgrand)
        self.player.update(1 << action)
        if pygame.sprite.collide_rect(self.player, self.goal):
            reward = 1.
            done = True
        elif self.global_step >= (1000 - 1):
            reward = -0.001
            done = True
        else:
            reward = -0.001
            done = False
        self.dirty_rects = self.sprites.draw(self.maze_surface)
        screen = pygame.transform.scale(self.maze_surface, [210, 160])
        observation = pygame.surfarray.array3d(screen).swapaxes(0, 1)
        self.global_step += 1

        info = self.action_available()

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

    def action_available(self):
        action_available = self.player.action_available()
        return {"": action_available}

    def close(self):
        pass

    def seed(self, seed=None):
        pass
