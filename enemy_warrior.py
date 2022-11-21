from pico2d import *
from npc import NPC
from game_world import game_object
from game_world import remove_object
import game_framework

PIXEL_PER_METER = 10.0 / 0.1  # 10픽셀당 10cm

RUN_SPEED_KMPH = 5.0
RUN_SPEED_MPH = RUN_SPEED_KMPH * 1000.0 / 60.0
RUN_SPEED_MPS = RUN_SPEED_MPH / 60.0
RUN_SPEED_PPS = RUN_SPEED_MPS * PIXEL_PER_METER

TIME_PER_ACTION = 0.4
TIME_PER_IDLE = 0.4
TIME_PER_HIT = 0.4
ACTION_PER_TIME = 1.0/TIME_PER_ACTION
IDLE_PER_TIME = 1.0/TIME_PER_IDLE
HIT_PER_TIME = 1.0/TIME_PER_HIT
FRAMES_PER_IDLE = 8
FRAMES_PER_ACTION = 16
FRAMES_PER_HIT = 12

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
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 16
        self.m_x -= self.dir_x * RUN_SPEED_PPS * game_framework.frame_time
        if self.cool_time > 0.0:
            self.cool_time -= game_framework.frame_time
        # if self.m_x < 50:
        #     self.m_x = 50

        # if self.check_enemy():
        #     self.cur_state.exit(self)
        #     if self.cool_time <= 0.0:
        #         self.cur_state = HIT
        #     else:
        #         self.cur_state = IDLE
        #     self.cur_state.enter(self)

    @staticmethod
    def draw(self):
        self.run.clip_draw_to_origin(self.run_size[0] * int(self.frame), 0, self.run_size[0], self.run_size[1],
                                            self.m_x, self.m_y)


class HIT:
    @staticmethod
    def enter(self):
        self.dir_x = 0
        self.frame = 0
        self.do_hit = False

    @staticmethod
    def exit(self):
        pass

    @staticmethod
    def do(self):
        oldFrame = self.frame
        self.frame = (self.frame + FRAMES_PER_HIT * HIT_PER_TIME * game_framework.frame_time) % 12
        if self.frame > 6 and self.do_hit == False:
            for enemy in game_object[3]:
                if self.get_hit_bb()[0] < enemy.get_bounding_box()[2] and enemy.layer == self.layer:
                    enemy.take_damage(self.give_damage())
            for castle in game_object[1]:
                if self.get_hit_bb()[0] < castle.get_bounding_box()[2]:
                    castle.take_damage(self.give_damage())
            self.do_hit = True

        if int(oldFrame) >= 10 and int(self.frame) <= 3:
            self.cool_time = 2.5
            self.cur_state.exit(self)
            if self.check_enemy():
                self.cur_state = IDLE
            else:
                self.cur_state = RUN
            self.cur_state.enter(self)

    @staticmethod
    def draw(self):
        self.hit.clip_draw_to_origin(self.hit_size[0] * int(self.frame), 0, self.hit_size[0], self.hit_size[1],
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
        oldFrame = self.frame
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 16
        if int(oldFrame) >= 12 and int(self.frame) <= 4:
            self.cur_state.exit(self)

    @staticmethod
    def draw(self):
        self.death.clip_draw_to_origin(self.death_size[0] * int(self.frame), 0, self.death_size[0], self.death_size[1],
                                       self.m_x, self.m_y)

next_state = {
    IDLE:{},
    HIT:{},
    RUN:{},
    DEAD:{}
}

# 히트박스 80, 110
# 충돌 지점 self.m_x - 120
# 5km/h의 이동 속도
# 공격 쿨타임 2.5초
# 히트 사이즈 70 -> 실제 히트 30
# 데미지 10, hp 70
class EnemyWarrior(NPC):
    idle = None
    warrior_run = None
    hit = None
    death = None
    idle_size = (120, 108)
    run_size = (123, 113)
    hit_size = (174, 136)
    death_size = (195, 149)

    def __init__(self, i_layer):
        if i_layer == 1:
            super().__init__(1200, 30, 10, 70, i_layer)
        else:
            # 200 ~ 260
            super().__init__(1200, 230, 10, 70, i_layer)

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
        for enemy in game_object[3]:
            if self.get_bounding_box()[0] < enemy.get_bounding_box()[2] and enemy.layer == self.layer:
                return True
        return False

    def get_bounding_box(self):
        return self.m_x + 40 - self.pos_dif, self.m_y - self.pos_dif, self.m_x + 120 - self.pos_dif,\
               self.m_y + 110 - self.pos_dif

    def get_hit_bb(self):
        return self.m_x + 10, self.m_y, self.m_x + 80, self.m_y + 110

    def collide(self, other, group):
        if group == "castle:eWar" and self.cur_state == RUN:
            self.cur_state.exit(self)
            if self.cool_time <= 0.0:
                self.cur_state = HIT
            else:
                self.cur_state = IDLE
            self.cur_state.enter(self)
        if group == 'war:eWar' and self.cur_state == RUN:
            self.cur_state.exit(self)
            if self.cool_time <= 0.0:
                self.cur_state = HIT
            else:
                self.cur_state = IDLE
            self.cur_state.enter(self)

    def take_damage(self, damage):
        self.health_point -= damage
        if self.health_point <= 0:
            self.die()

    def give_damage(self):
        return self.attack_damage

    def die(self):
        self.cur_state.exit(self)
        self.cur_state = DEAD
        self.cur_state.enter(self)