from pico2d import *
import game_framework
import over_state

width = 1280
height = 720
bar_width = 1808
bar_height = 124
col_bar_width = 1730
col_bar_height = 66

class Castle:
    def __init__(self):
        self.castle = load_image("image/castle.png")
        self.hp_bar = load_image("image/bar.png")
        self.hp = load_image("image/hp.png")
        self.collision_sound_effect = load_wav('sound_effect/castle_collision.wav')
        self.collision_sound_effect.set_volume(32)
        self.m_x = 0
        self.m_y = 245
        self.max_hp = 100
        self.now_hp = 100

    def update(self):
        if self.now_hp <= 0:
            game_framework.push_state(over_state)

    def draw(self):
        self.castle.draw(self.m_x, self.m_y)
        self.hp_bar.clip_draw_to_origin(0, 0, bar_width, bar_height, width//2 - 301, 680,
                                        bar_width // 3, bar_height // 3)
        self.hp.clip_draw_to_origin(0, 0, col_bar_width * self.now_hp // self.max_hp, col_bar_height, width//2 + 13 - 301, 680 + 10,
                                    col_bar_width // 3 * self.now_hp // self.max_hp, col_bar_height // 3)

    def get_bounding_box(self):
        return 0, self.m_y - 516 / 2, 177 / 2,  self.m_y + 516 / 2

    def collide(self, other, group):
        pass

    def take_damage(self, damage):
        self.collision_sound_effect.play()
        self.now_hp -= damage