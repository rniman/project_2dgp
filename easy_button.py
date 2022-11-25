from button import Button

class Easy(Button):
    def __init__(self):
        super().__init__()

    def update(self):
        pass

    def draw(self):
        self.button.clip_draw(0, 0, 454, 142, 1280 / 2, 360 + 100, 454 / 3 * 2, 142 / 2)
        self.font.draw(640 - 30, 360 + 100, f'EASY', (0, 0, 0))
