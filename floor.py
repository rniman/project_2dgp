from pico2d import *

width = 1280


class Floor:
    def __init__(self):
        self.floor = load_image('image/tile.png')
        self.tile_width = 90

    def draw(self):
        for x in range(98, width, self.tile_width):
            self.floor.draw(x, 245)
            x = x + self.tile_width
