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
        self.idle.clip_draw_to_origin(self.idle_size[0] * self.frame, 0, self.idle_size[0], self.idle_size[1],
                                              self.m_x, self.m_y, self.idle_size[0], self.idle_size[1])
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
        self.m_x -= self.dir_x * 5
        if self.cool_time > 0:
            self.cool_time -= 1
        if self.m_x < 50:
            self.m_x = 50
            print(self.m_x)

        if self.check_enemy():
            self.cur_state.exit(self)
            if self.cool_time == 0:
                self.cur_state = HIT
            else:
                self.cur_state = IDLE
            self.cur_state.enter(self)

    @staticmethod
    def draw(self):
        self.run.clip_draw_to_origin(self.run_size[0] * self.frame, 0, self.run_size[0], self.run_size[1],
                                            self.m_x, self.m_y)


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
        self.frame = (self.frame + 1) % 12
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
        self.hit.clip_draw_to_origin(self.hit_size[0] * self.frame, 0, self.hit_size[0], self.hit_size[1],
                                             self.m_x, self.m_y, self.hit_size[0], self.hit_size[1])


class DEAD:
    @staticmethod
    def enter(self):
        self.frame = 0

    @staticmethod
    def exit(self):
        remove_object(self)

    @staticmethod
    def do(self):
        self.frame = (self.frame + 1) % 16
        if self.frame == 0:
            self.cur_state.exit(self)

    @staticmethod
    def draw(self):
        self.death.clip_draw_to_origin(self.death_size[0] * self.frame, 0, self.death_size[0], self.death_size[1],
                                       self.m_x, self.m_y)

# 히트박스 120, 110
class EnemyWarrior(NPC):
    idle = None
    warrior_run = None
    hit = None
    death = None
    idle_size = (120, 108)
    run_size = (123, 113)
    hit_size = (174, 136)
    death_size = (195, 149)
    def __init__(self):
        super().__init__(1200, 40, 10, 70)
        if EnemyWarrior.idle == None:
            self.idle = load_image('image/Ewarrior_idle.png')
            self.run = load_image('image/Ewarrior_run.png')
            self.hit = load_image('image/Ewarrior_hit.png')
            self.death = load_image('image/Ewarrior_death.png')

        self.cur_state = RUN
        self.cur_state.enter(self)

    def update(self):
        self.cur_state.do(self)

    def draw(self):
        self.cur_state.draw(self)

    def check_enemy(self):
        if self.m_x == 50:
            return True
        for enemy in game_object[2]:
            if self.m_x - 120 < enemy.m_x:
                return True
        return False

