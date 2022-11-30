from pico2d import *

class Decor:
    def __init__(self, i_y):
        self.floor = load_image('image/decor.png')
        self.m_y = i_y

    def update(self):
        pass

    def draw(self):
        self.floor.clip_draw_to_origin(0, 0, 640, 110, 0 + (self.m_y - 200) / 2, self.m_y)
        self.floor.clip_draw_to_origin(0, 0, 640, 110, 630 + (self.m_y - 200) / 2, self.m_y)
        self.floor.clip_draw_to_origin(0, 0, 20, 110, 1260 + (self.m_y - 200) / 2, self.m_y)

    def get_bounding_box(self):
        return 0, 200, 1280 - 1, 310
