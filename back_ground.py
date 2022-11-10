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