from pico2d import *
from npc import NPC
from game_world import game_object
from game_world import remove_object
from game_world import remove_collision_object
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
                                     self.m_x, self.m_y - 5)


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
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 16
        if self.frame > 8 and self.do_hit == False:
            for enemy in game_object[2]:
                if self.get_hit_bb()[2] > enemy.get_bounding_box()[0] and enemy.layer == self.layer:
                    enemy.take_damage(self.give_damage())

            self.do_hit = True

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
        remove_collision_object(self)
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


next_state = {

}

# 히트박스  80, 110
# 충돌지점 -> m_x + 120
# 6km/h의 이동 속도
# 공격 쿨타임 3초
# 히트 사이즈 80 -> 실제 히트 60
# 데미지 7, 체력 50
class Warrior(NPC):
    idle = None
    run = None
    hit = None
    death = None
    idle_size = (122, 106)
    run_size = (131, 158)
    hit_size = (198, 175)
    death_size = (187, 175)

    def __init__(self, i_layer):
        # 1층 115  2층 325
        if i_layer == 1:
            super().__init__(0, 40, 7, 50, i_layer)
        elif i_layer == 2:
            # 190, 250 은 불가능할듯
            # 205 265에서 선택하면 될듯
            super().__init__(0, 235, 7, 50, i_layer)

        if Warrior.idle == None:
            self.idle = load_image('image/warrior_idle.png')
            self.run = load_image('image/warrior_run.png')
            self.hit = load_image('image/warrior_hit.png')
            self.death = load_image('image/warrior_death.png')

        self.hit_box = None
        self.cur_state = RUN
        self.cur_state.enter(self)
        self.enemy_list = dict()

    def update(self):
        self.cur_state.do(self)

    def draw(self):
        self.cur_state.draw(self)

    def check_enemy(self):
        for enemy in game_object[2]:
            if self.get_bounding_box()[2] > enemy.get_bounding_box()[0] and enemy.layer == self.layer:
                return True
        return False

    def get_bounding_box(self):
        return self.m_x + 40 - self.pos_dif, self.m_y - self.pos_dif, self.m_x + 120 - self.pos_dif, self.m_y + 110 - self.pos_dif

    def get_hit_bb(self):
        return self.m_x + 100, self.m_y, self.m_x + 180, self.m_y + 110

    def collide(self, other, group):
        if group == 'war:eWar' and self.cur_state == RUN:
            # add_event
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