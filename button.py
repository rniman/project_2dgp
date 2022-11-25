from pico2d import *

class Button:
    button = None
    font = None
    def __init__(self):
        if Button.button == None:
            self.button = load_image('image/button.png')
            self.font = load_font('font/Arial_Black.ttf', 25)

    def update(self):
        pass

    def draw(self):
        pass
