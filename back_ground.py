from pico2d import *

width = 1280
height = 720

class BackGround:
    def __init__(self):
        self.backGround = load_image('image/Bground.png')

    def update(self):
        pass

    def draw(self):
        self.backGround.draw(width // 2, height // 2)

    def get_bounding_box(self):
        return 0, 0, 1279, 719


