from pico2d import *
from npc import NPC
from game_world import game_object
from game_world import remove_object
from game_world import remove_collision_object
import game_framework
from behavior_tree import BehaviorTree, Selector, Sequence, Leaf


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
    def do(self):
        self.frame = (self.frame + FRAMES_PER_IDLE * IDLE_PER_TIME * game_framework.frame_time) % 8

    @staticmethod
    def draw(self):
        Warrior.idle.clip_draw_to_origin(Warrior.idle_size[0] * int(self.frame), 0, Warrior.idle_size[0], Warrior.idle_size[1],
                                      self.m_x + 50, self.m_y)

class RUN:
    @staticmethod
    def do(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 16

    @staticmethod
    def draw(self):
        Warrior.run.clip_draw_to_origin(Warrior.run_size[0] * int(self.frame), 0, Warrior.run_size[0], Warrior.run_size[1],
                                     self.m_x, self.m_y - 5)

class HIT:
    @staticmethod
    def do(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 16

    @staticmethod
    def draw(self):
        Warrior.hit.clip_draw_to_origin(Warrior.hit_size[0] * int(self.frame), 0, Warrior.hit_size[0], Warrior.hit_size[1],
                                     self.m_x, self.m_y)

class DEAD:
    @staticmethod
    def do(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)

    @staticmethod
    def draw(self):
        Warrior.death.clip_draw_to_origin(Warrior.death_size[0] * int(self.frame), 0, Warrior.death_size[0], Warrior.death_size[1],
                                       self.m_x, self.m_y - 20)


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

    hit_sound_effect = None
    collision_sound_effect = None
    dead_sound_effect = None

    def __init__(self, i_layer):
        # 1층 115  2층 325
        if i_layer == 1:
            super().__init__(0, 30, 5, 70, i_layer)
        elif i_layer == 2:
            super().__init__(0, 235, 5, 70, i_layer)

        if Warrior.idle == None:
            Warrior.idle = load_image('image/warrior_idle.png')
            Warrior.run = load_image('image/warrior_run.png')
            Warrior.hit = load_image('image/warrior_hit.png')
            Warrior.death = load_image('image/warrior_death.png')
            Warrior.hit_sound_effect = load_wav('sound_effect/warrior_swing.wav')
            Warrior.collision_sound_effect = load_wav('sound_effect/warrior_collision.wav')
            Warrior.dead_sound_effect = load_wav('sound_effect/warrior_die (mp3cut.net).wav')
            Warrior.hit_sound_effect.set_volume(32)
            Warrior.collision_sound_effect.set_volume(32)
            Warrior.dead_sound_effect.set_volume(32)

        self.cur_state = RUN
        self.build_behavior_tree()

    def get_bounding_box(self):
        return self.m_x + 40 - self.pos_dif, self.m_y - self.pos_dif, self.m_x + 120 - self.pos_dif, self.m_y + 110 - self.pos_dif

    def get_hit_bb(self):
        return self.m_x + 100, self.m_y, self.m_x + 180, self.m_y + 110

    def collide(self, other, group):
        if group == 'war:eWar':
            self.collision = True

    def take_damage(self, damage):
        Warrior.collision_sound_effect.play()
        self.health_point -= damage
        if self.health_point <= 0:
            self.die()

    def die(self):
        if self.health_point > 0:
            return BehaviorTree.FAIL

        if self.cur_state != DEAD:
            Warrior.dead_sound_effect.play()
            self.cur_state = DEAD
            self.frame = 0

        if self.frame >= 16:
            remove_object(self)
            remove_collision_object(self)
            return BehaviorTree.SUCCESS

        return BehaviorTree.RUNNING

    def run_to_right(self):
        if self.cur_state != RUN:
            self.cur_state = RUN
            self.dir_x = 1

        self.m_x += self.dir_x * RUN_SPEED_PPS * game_framework.frame_time
        if self.cool_time > 0.0:
            self.cool_time -= game_framework.frame_time
        if self.m_x > 1150:
            self.m_x = 1150

        return BehaviorTree.SUCCESS

    def check_cool_time(self):
        if not self.collision:
            return BehaviorTree.FAIL

        if self.cool_time <= 0.0:
            return BehaviorTree.SUCCESS

        if self.cur_state != IDLE:
            self.cur_state = IDLE
            self.dir_x = 0
            self.frame = 0
        return BehaviorTree.RUNNING

    def attack_enemy(self):
        if not self.collision:
            return BehaviorTree.FAIL

        if self.cur_state != HIT:
            Warrior.hit_sound_effect.play()
            self.cur_state = HIT
            self.dir_x = 0
            self.frame = 0
            self.do_hit = False

        if self.frame > 10 and self.do_hit == False:
            for enemy in game_object[2]:
                if self.get_hit_bb()[2] > enemy.get_bounding_box()[0] and enemy.layer == self.layer:
                    enemy.take_damage(self.give_damage())
            self.do_hit = True

        if int(self.frame) <= 3.0 and self.do_hit == True:
            self.cool_time = 3.0
            self.do_hit = False
            return BehaviorTree.SUCCESS

        return BehaviorTree.RUNNING

    def build_behavior_tree(self):
        check_cool_time_node = Leaf("Check Cool Time", self.check_cool_time)
        attack_enemy_node = Leaf("Attack Enemy", self.attack_enemy)
        attack_sequence = Sequence("Check Cool Time and Attack", check_cool_time_node, attack_enemy_node)

        run_node = Leaf("Run to Right", self.run_to_right)
        dead_node = Leaf("Dead", self.die)
        root_node = Selector("Attack or Run", dead_node, attack_sequence, run_node)
        self.bt = BehaviorTree(root_node)
