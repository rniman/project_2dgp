from pico2d import *

width = 1280

class Floor:
    def __init__(self):
        self.floor = load_image('image/floor.png')

    def update(self):
        pass

    def draw(self):
        self.floor.clip_draw_to_origin(0, 0, 1280, 70, 0, 200)

    def get_bounding_box(self):
        return 0, 235, 1280 - 1, 255

    def collide(self, other, group):
        pass
