import logo_state
from pico2d import *
from character import Character

width = 1280
height = 720
bar_width = 1808
bar_height = 124
col_bar_width = 1730
col_bar_height = 66

class MainCharacter(Character):
    def __init__(self):
        super().__init__(100, 90, 10)
        self.main_idle = load_image('image/main_idle.png')
        self.main_run = load_image('image/main_run.png')
        self.main_hit = load_image('image/main_hit.png')
        self.main_climb = load_image('image/main_climb.png')
        self.resource_bar = load_image('image/bar.png')
        self.resource = load_image('image/resource.png')
        self.idle_size = (373, 286)
        self.run_size = (428, 331)
        self.climb_size = (376, 262)
        self.hit_size = (647, 504)
        self.box = [self.m_x, self.m_y, self.m_x + self.idle_size[0]//6, self.m_y + self.idle_size[1]//3]
        self.now_resource = 100
        self.max_resource = 300

        self.dir_x = logo_state.dir_x
        self.dir_y = logo_state.dir_y
        self.look_at = 1
        if self.dir_x != 0:
            self.state = 1
            if self.dir_x > 0:
                self.look_at = 1
            else:
                self.look_at = -1

    def idle(self):
        self.main_idle.clip_draw(0 + self.frame * self.idle_size[0], 0, self.idle_size[0], self.idle_size[1],
                                 self.m_x, self.m_y, self.idle_size[0] // 3, self.idle_size[1] // 3)

    def flip_idle(self):
        self.main_idle.clip_composite_draw(0 + self.frame * self.idle_size[0], 0, self.idle_size[0], self.idle_size[1],
                                           0, 'h', self.m_x, self.m_y, self.idle_size[0] // 3, self.idle_size[1] // 3)

    def run(self):
        self.main_run.clip_draw(0 + self.frame * self.run_size[0], 0, self.run_size[0], self.run_size[1],
                                self.m_x, self.m_y, self.run_size[0] // 3, self.run_size[1] // 3)

    def flip_run(self):
        self.main_run.clip_composite_draw(0 + self.frame * self.run_size[0], 0, self.run_size[0], self.run_size[1],
                                          0, 'h', self.m_x, self.m_y, self.run_size[0] // 3, self.run_size[1] // 3)

    def climb(self):
        self.main_climb.clip_draw(0 + self.frame * self.climb_size[0], 0, self.climb_size[0], self.climb_size[1],
                                  self.m_x, self.m_y, self.climb_size[0] // 3, self.climb_size[1] // 3)

    def hit(self):  # y, 120
        self.main_hit.clip_draw(0 + self.frame * self.hit_size[0], 0, self.hit_size[0], self.hit_size[1],
                                self.m_x, self.m_y + 20, self.hit_size[0] // 3, self.hit_size[1] // 3)

    def flip_hit(self):  # y, 120
        self.main_hit.clip_composite_draw(0 + self.frame * self.hit_size[0], 0, self.hit_size[0], self.hit_size[1],
                                          0, 'h', self.m_x, self.m_y + 20, self.hit_size[0] // 3, self.hit_size[1] // 3)

    def update(self):
        self.frame_rate()
        self.move()
        self.get_now_resource()

    def draw(self):
        #
        self.resource_bar.clip_draw_to_origin(0, 0, bar_width, bar_height, width // 2 - 301, 640,
                                              bar_width // 3, bar_height // 3)
        # 13, 10은 테두리 맞춰줌
        self.resource.clip_draw_to_origin(0, 0, col_bar_width * self.now_resource // self.max_resource, col_bar_height,
                                          width // 2 + 13 - 301, 640 + 10,
                                          col_bar_width // 3  * self.now_resource // self.max_resource,
                                          col_bar_height // 3)

        if self.state == 0 and self.look_at == 1:
            self.idle()
        elif self.state == 0 and self.look_at == -1:
            self.flip_idle()
        elif self.state == 1 and self.look_at == 1:
            self.run()
        elif self.state == 1 and self.look_at == -1:
            self.flip_run()
        elif self.state == 2:
            self.climb()
        elif self.state == 3 and self.look_at == 1:
            self.hit()
        elif self.state == 3 and self.look_at == -1:
            self.flip_hit()

    def frame_rate(self):
        if self.state == 0:
            self.frame = (self.frame + 1) % 8
        elif self.state == 1:
            self.frame = (self.frame + 1) % 8
        elif self.state == 2:
            self.frame = (self.frame + 1) % 8
        elif self.state == 3:
            self.frame = (self.frame + 1) % 12
            if self.frame == 0:
                if self.dir_x == 0:
                    self.state = 0
                else:
                    self.state = 1

    def set_box(self):
        if self.look_at == 1:
            self.box = [self.m_x, self.m_y, self.m_x + self.idle_size[0] // 6, self.m_y + self.idle_size[1] // 3]
        else:
            self.box = [self.m_x - self.idle_size[0] // 6, self.m_y, self.m_x, self.m_y - self.idle_size[1] // 3]

    def move(self):
        if self.state == 1 or self.state == 0:
            self.m_x += self.dir_x * 5
            if self.m_x > 1200:
                self.m_x = 1200
            elif self.m_x < 100:
                self.m_x = 100
            self.set_box()
        elif self.state == 2:
            self.ladder_move()

    def ladder_move(self):
        self.m_y += self.dir_y * 5
        if self.m_y > 300:
            self.m_y = 300
            if self.dir_x == 0:
                self.state = 0
            else:
                self.state = 1
            if self.look_at == -1:
                self.m_x += 35  # flip x좌표 이미지 보정
        elif self.m_y < 90:
            if self.dir_x == 0:
                self.state = 0
            else:
                self.state = 1
            self.m_y = 90
            if self.look_at == -1:
                self.m_x += 35  # flip x좌표 이미지 보정

    def get_now_resource(self):
        if self.now_resource < 300:
            self.now_resource += 1
