from button import Button

class Tutorial(Button):
    def __init__(self):
        super().__init__()

    def update(self):
        pass

    def draw(self):
        self.button.clip_draw(0, 0, 454, 142, 1280 / 2, 720 / 2, 454 / 3 * 2, 142 / 2)
        self.font.draw(640 - 60, 360, f'TUTORIAL', (0, 0, 0))
