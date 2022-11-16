from pico2d import *
from npc import NPC
from game_world import game_object
from game_world import remove_object
import game_framework

PIXEL_PER_METER = 10.0 / 0.1  # 10픽셀당 10cm

RUN_SPEED_KMPH = 6.0
RUN_SPEED_MPH = RUN_SPEED_KMPH * 1000.0 / 60.0
RUN_SPEED_MPS = RUN_SPEED_MPH / 60.0
RUN_SPEED_PPS = RUN_SPEED_MPS * PIXEL_PER_METER

TIME_PER_ACTION = 0.4
TIME_PER_IDLE = 0.4
ACTION_PER_TIME = 1.0/TIME_PER_ACTION
IDLE_PER_TIME = 1.0/TIME_PER_IDLE
FRAMES_PER_IDLE = 8
FRAMES_PER_ACTION = 16

class IDLE:
    @staticmethod
    def enter(self):
        self.dir_x = 0
        pass

    @staticmethod
    def exit(self):
        pass

    @staticmethod
    def do(self):
        self.frame = (self.frame + FRAMES_PER_IDLE * IDLE_PER_TIME * game_framework.frame_time) % 8
        if self.cool_time > 0.0:
            self.cool_time -= game_framework.frame_time
        if self.check_enemy():
            if self.cool_time <= 0.0:
                self.cur_state.exit(self)
                self.cur_state = HIT
                self.cur_state.enter(self)
        else:
            self.cur_state.exit(self)
            self.cur_state = RUN
            self.cur_state.enter(self)

    @staticmethod

    def draw(self):
        self.idle.clip_draw_to_origin(self.idle_size[0] * int(self.frame), 0, self.idle_size[0], self.idle_size[1],
                                      self.m_x + 50, self.m_y)

class RUN:
    @staticmethod
    def enter(self):
        self.dir_x = 1
        pass

    @staticmethod
    def exit(self):
        pass

    @staticmethod
    def do(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 16
        self.m_x += self.dir_x * RUN_SPEED_PPS * game_framework.frame_time
        if self.cool_time > 0.0:
            self.cool_time -= game_framework.frame_time
        if self.m_x > 1150:
            self.m_x = 1150

        if self.check_enemy():
            self.cur_state.exit(self)
            if self.cool_time <= 0.0:
                self.cur_state = HIT
            else:
                self.cur_state = IDLE
            self.cur_state.enter(self)

    @staticmethod
    def draw(self):
        self.run.clip_draw_to_origin(self.run_size[0] * int(self.frame), 0, self.run_size[0], self.run_size[1],
                                     self.m_x, self.m_y)


class HIT:
    @staticmethod
    def enter(self):
        self.dir_x = 0
        self.frame = 0

    @staticmethod
    def exit(self):
        pass

    @staticmethod
    def do(self):
        oldFrame = self.frame
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 16
        if int(oldFrame) >= 10 and int(self.frame) <= 5:
            self.cool_time = 3.0
            self.cur_state.exit(self)
            if self.check_enemy():
                self.cur_state = IDLE
            else:
                self.cur_state = RUN
            self.cur_state.enter(self)

    @staticmethod
    def draw(self):
        self.hit.clip_draw_to_origin(self.hit_size[0] * int(self.frame), 0, self.hit_size[0], self.hit_size[1],
                                     self.m_x, self.m_y)


class DEAD:
    @staticmethod
    def enter(self):
        self.frame = 0

    @staticmethod
    def exit(self):
        remove_object(self)
        pass

    @staticmethod
    def do(self):
        oldFrame = self.frame
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 16
        if int(oldFrame) >= 10 and int(self.frame) <= 5:
            self.cur_state.exit(self)

    @staticmethod
    def draw(self):
        self.death.clip_draw_to_origin(self.death_size[0] * int(self.frame), 0, self.death_size[0], self.death_size[1],
                                       self.m_x, self.m_y - 20)


# 히트박스 120, 110
# 충돌지점 -> m_x + 120
class Warrior(NPC):
    idle = None
    run = None
    hit = None
    death = None
    idle_size = (122, 106)
    run_size = (131, 158)
    hit_size = (198, 175)
    death_size = (187, 175)
    def __init__(self, i_key):
        # 1층 115  2층 325
        if i_key == 1:
            super().__init__(0, 40, 5, 50)
        elif i_key == 5:
            super().__init__(0, 250, 5, 50)

        if Warrior.idle == None:
            self.idle = load_image('image/warrior_idle.png')
            self.run = load_image('image/warrior_run.png')
            self.hit = load_image('image/warrior_hit.png')
            self.death = load_image('image/warrior_death.png')

        self.hit_box = None

        self.cur_state = RUN
        self.cur_state.enter(self)

    def update(self):
        self.cur_state.do(self)

    def draw(self):
        self.cur_state.draw(self)

    def check_enemy(self):
        for enemy in game_object[1]:
            if self.m_x + 120 > enemy.m_x:
                return True
        return False


