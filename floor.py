from pico2d import *

width = 1280

class Floor:
    def __init__(self):
        self.floor = load_image('image/tile.png')
        self.tile_width = 90

    def update(self):
        pass

    def draw(self):
        for x in range(98, width, self.tile_width):
            self.floor.draw(x, 245)
            x = x + self.tile_width

    def get_bounding_box(self):
        return 0, 235, 1280 - 1, 255

    def collide(self, other, group):
        pass

    def no_collide(self, other, group):
        pass