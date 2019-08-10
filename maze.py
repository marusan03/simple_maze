'''maze'''

import numpy as np
import pygame
from pygame import surfarray
# from PIL import Image

from utils import Directions


def build_maze(width, height):
    '''build maze'''

    directions = Directions()  # 上 右 下 左
    directions = directions.get()
    maze = [[1 for i in range(width * 2 + 1)] for j in range(height * 2 + 1)]
    # 外枠埋め
    for i in range(height * 2 + 1):
        for j in range(width * 2 + 1):
            if i == 0 or i == height * 2 or j == 0 or j == width * 2:
                maze[i][j] = 0
            elif i % 2 == 0 and j % 2 == 0:
                maze[i][j] = 0
            else:
                pass

    # 棒倒し法
    for i in range(2, height * 2, 2):
        for j in range(2, width * 2, 2):
            while True:
                if i == 2:
                    index = np.random.choice(4)
                else:
                    index = np.random.choice([1, 2, 3])
                if maze[i+directions[index][0]][j+directions[index][1]] == 0:
                    continue
                else:
                    maze[i+directions[index][0]][j+directions[index][1]] = 0
                    break

    # maze_array = np.array(maze, dtype=np.int8)
    # print_maze(height, maze_array)

    # pil_image = Image.fromarray(maze_array*255)
    # pil_image.show()
    # pil_image.convert("RGB").save(
    #     "./test3.png", 'JPEG', quality=100, optimize=True)

    # 通行可能かどうかの判定map
    accesible_map = [[0 for i in range(width * 2 + 1)]
                     for j in range(height * 2 + 1)]
    for i in range(height * 2 + 1):
        for j in range(width * 2 + 1):
            flag = 0b0
            if maze[i][j] == 0:
                accesible_map[i][j] = 0
            else:
                for k, direction in enumerate(directions):
                    if maze[i+direction[0]][j+direction[1]] == 1:
                        flag = flag | (1 << k)
                accesible_map[i][j] = int(flag)
    # print_maze(height, accesible_map)
    return surfarray.make_surface(np.array(maze)*255), tuple(accesible_map)


def print_maze(height, maze):
    '''show maze'''
    for i in range(height * 2 + 1):
        print(maze[i])


if __name__ == "__main__":
    build_maze(10, 10)
