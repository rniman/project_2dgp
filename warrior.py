from pico2d import *
from npc import NPC
from game_world import game_object
from game_world import remove_object

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
        self.frame = (self.frame + 1) % 8
        if self.cool_time > 0:
            self.cool_time -= 1
        if self.check_enemy():
            if self.cool_time == 0:
                self.cur_state.exit(self)
                self.cur_state = HIT
                self.cur_state.enter(self)
        else:
            self.cur_state.exit(self)
            self.cur_state = RUN
            self.cur_state.enter(self)

    @staticmethod
    def draw(self):
        self.warrior_idle.clip_composite_draw(self.idle_size[0] * self.frame, 0, self.idle_size[0], self.idle_size[1],
                                              0, 'h', self.m_x + 35, self.m_y - 20, self.idle_size[0], self.idle_size[1])

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
        self.frame = (self.frame + 1) % 16
        self.m_x += self.dir_x * 5
        if self.cool_time > 0:
            self.cool_time -= 1
        if self.m_x > 1200:
            self.m_x = 1200

        if self.check_enemy():
            self.cur_state.exit(self)
            if self.cool_time == 0:
                self.cur_state = HIT
            else:
                self.cur_state = IDLE
            self.cur_state.enter(self)

    @staticmethod
    def draw(self):
        self.warrior_run.clip_composite_draw(self.run_size[0] * self.frame, 0, self.run_size[0], self.run_size[1],
                                             0, 'h', self.m_x, self.m_y, self.run_size[0], self.run_size[1])


class HIT:
    @staticmethod
    def enter(self):
        self.dir_x = 0
        self.frame = 0
        pass

    @staticmethod
    def exit(self):
        pass

    @staticmethod
    def do(self):
        self.frame = (self.frame + 1) % 16
        if self.frame == 0:
            self.cool_time = 100
            self.cur_state.exit(self)
            if self.check_enemy():
                self.cur_state = IDLE
            else:
                self.cur_state = RUN
            self.cur_state.enter(self)

    @staticmethod
    def draw(self):
        self.warrior_hit.clip_composite_draw(self.hit_size[0] * self.frame, 0, self.hit_size[0], self.hit_size[1],
                                             0, 'h', self.m_x + 17, self.m_y + 15, self.hit_size[0], self.hit_size[1])


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
        self.frame = (self.frame + 1) % 16
        if self.frame == 0:
            self.cur_state.exit(self)

    @staticmethod
    def draw(self):
        self.warrior_death.clip_composite_draw(self.death_size[0] * self.frame, 0, self.death_size[0], self.death_size[1],
                                               0, 'h', self.m_x, self.m_y, self.death_size[0], self.death_size[1])

class Warrior(NPC):
    warrior_idle = None
    warrior_run = None
    warrior_hit = None
    warrior_death = None
    idle_size = (121, 106)
    run_size = (131, 158)
    hit_size = (198, 175)
    death_size = (187, 175)
    def __init__(self, i_key):
        # 1층 115  2층 325
        if i_key == 1:
            super().__init__(90, 115, 5, 50)
        elif i_key == 5:
            super().__init__(90, 325, 5, 50)

        if Warrior.warrior_idle == None:
            self.warrior_idle = load_image('image/warrior_idle.png')
            self.warrior_run = load_image('image/warrior_run.png')
            self.warrior_hit = load_image('image/warrior_hit.png')
            self.warrior_death = load_image('image/warrior_death.png')

        self.cur_state = RUN
        # self.prev_state = None
        self.cur_state.enter(self)

    def update(self):
        self.cur_state.do(self)

    def draw(self):
        self.cur_state.draw(self)

    def check_enemy(self):
        for enemy in game_object[1]:
            if self.m_x + 50 > enemy.m_x:
                return True
        return False


