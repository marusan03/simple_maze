import glob
import re
import os
from PIL import Image


class Directions(object):
    def __init__(self):
        self.up = (0, -1)
        self.right = (1, 0)
        self.down = (0, 1)
        self.left = (-1, 0)

    def direction_to_flag(self, direction):
        if self.up == direction:
            return 1
        elif self.right == direction:
            return 2
        elif self.down == direction:
            return 4
        elif self.left == direction:
            return 8
        else:
            raise ValueError

    def flag_to_direction(self, flag):
        if 1 == flag:
            return self.up
        elif 2 == flag:
            return self.right
        elif 4 == flag:
            return self.down
        elif 8 == flag:
            return self.left
        else:
            raise ValueError

    def get(self):
        return self.up, self.right, self.down, self.left


def screenshot(screen):
    if not os.path.isdir('./images'):
        os.mkdir("./images")
        number = 0
    else:
        image_list = sorted(glob.glob('./images/*.png'), reverse=True)
        if image_list:
            numbers = re.findall(r'[0-9][0-9][0-9]', image_list[0])
            number = max([int(num) for num in numbers]) + 1
        else:
            number = 0

    image = Image.fromarray(screen)
    image.save(f'./images/screen_{number:03}.png')
