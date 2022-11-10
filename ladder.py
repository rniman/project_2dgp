from pico2d import *

class Ladder:
    def __init__(self):
        self.ladder = load_image('image/ladder.png')
        self.mx = (300, 800)

    def update(self):
        pass

    def draw(self):
        self.ladder.draw(self.mx[0], 160)
        self.ladder.draw(self.mx[1], 160)
