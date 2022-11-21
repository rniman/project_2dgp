from pico2d import *


class Ladder:
    ladder = None

    def __init__(self, i_x):
        if Ladder.ladder == None:
            self.ladder = load_image('image/ladder.png')
        self.mx = i_x

    def update(self):
        pass

    def draw(self):
        self.ladder.draw(self.mx, 140)
        # draw_rectangle(*self.get_bounding_box())

    def get_bounding_box(self):
        return self.mx - 35, 140 - 175/2, self.mx + 35, 140 + 175/2

    def collide(self, other, group):
        pass

    def no_collide(self, other, group):
        pass
