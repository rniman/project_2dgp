from pico2d import *
import game_framework
import clear_state

class Clear_time:
    def __init__(self, i_clear_time = 10):
        self.time_font = load_font('font/kozuka_gothic_bold.otf', 40)
        self.clear_time = i_clear_time

    def update(self):
        self.clear_time -= game_framework.frame_time
        if self.clear_time <= 0:
            game_framework.push_state(clear_state)

    def draw(self):
        self.time_font.draw(600, 620, f'{int(self.clear_time) // 60:.0f} : {int(self.clear_time) % 60:.0f}',
                            (249, 243, 231))

