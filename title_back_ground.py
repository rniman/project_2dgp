from pico2d import *

width = 1280
height = 720

class BackGround:
    def __init__(self):
        self.backGround = load_image('image/title_background.png')
        self.back_board = load_image('image/window_background.png')
        self.bgm = load_music('music/title_bgm.mp3')
        self.bgm.set_volume(32)
        self.bgm.repeat_play()

    def update(self):
        pass

    def draw(self):
        self.backGround.clip_draw(0, 0, 1280, 720, 1280 / 2, 720 / 2, 1280, 720)
        self.back_board.clip_draw(0, 0, 500, 500, 1280 / 2, 720 / 2)

    def get_bounding_box(self):
        return 0, 0, 1279, 719


