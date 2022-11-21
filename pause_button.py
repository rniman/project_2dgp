from pico2d import *

class Pause:
    def __init__(self):
        self.pause = load_image('image/pause.png')

    def update(self):
        pass

    def draw(self):
        self.pause.clip_draw(0, 0, 39, 50, 1220, 660)
