from pico2d import *
from npc import NPC
from game_world import game_object
from game_world import remove_object
from game_world import remove_collision_object
import game_framework
from behavior_tree import BehaviorTree, Selector, Sequence, Leaf

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
    def do(self):
        self.frame = (self.frame + FRAMES_PER_IDLE * IDLE_PER_TIME * game_framework.frame_time) % 8

    @staticmethod
    def draw(self):
        EnemyWarrior.idle.clip_draw_to_origin(EnemyWarrior.idle_size[0] * int(self.frame), 0, EnemyWarrior.idle_size[0], EnemyWarrior.idle_size[1],
                                              self.m_x, self.m_y)
class RUN:
    @staticmethod
    def do(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 16

    @staticmethod
    def draw(self):
        EnemyWarrior.run.clip_draw_to_origin(EnemyWarrior.run_size[0] * int(self.frame), 0, EnemyWarrior.run_size[0], EnemyWarrior.run_size[1],
                                            self.m_x, self.m_y)

class HIT:
    @staticmethod
    def do(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 12

    @staticmethod
    def draw(self):
        EnemyWarrior.hit.clip_draw_to_origin(EnemyWarrior.hit_size[0] * int(self.frame), 0, EnemyWarrior.hit_size[0], EnemyWarrior.hit_size[1],
                                             self.m_x, self.m_y)

class DEAD:
    @staticmethod
    def do(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)

    @staticmethod
    def draw(self):
        EnemyWarrior.death.clip_draw_to_origin(EnemyWarrior.death_size[0] * int(self.frame), 0, EnemyWarrior.death_size[0], EnemyWarrior.death_size[1],
                                       self.m_x, self.m_y)


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

    hit_sound_effect = None
    collision_sound_effect = None
    dead_sound_effect = None

    def __init__(self, i_layer):
        if i_layer == 1:
            super().__init__(1200, 25, 10, 60, i_layer)
        else:
            # 200 ~ 260
            super().__init__(1200, 230, 10, 60, i_layer)

        if EnemyWarrior.idle == None:
            EnemyWarrior.idle = load_image('image/Ewarrior_idle.png')
            EnemyWarrior.run = load_image('image/Ewarrior_run.png')
            EnemyWarrior.hit = load_image('image/Ewarrior_hit.png')
            EnemyWarrior.death = load_image('image/Ewarrior_death.png')
            EnemyWarrior.hit_sound_effect = load_wav('sound_effect/Ewarrior_swing.wav')
            EnemyWarrior.collision_sound_effect = load_wav('sound_effect/Ewarrior_collision.wav')
            EnemyWarrior.dead_sound_effect = load_wav('sound_effect/Ewarrior_die.wav')

        self.cur_state = RUN
        self.build_behavior_tree()

    def get_bounding_box(self):
        return self.m_x + 40 - self.pos_dif, self.m_y - self.pos_dif, self.m_x + 120 - self.pos_dif,\
               self.m_y + 110 - self.pos_dif

    def get_hit_bb(self):
        return self.m_x + 10, self.m_y, self.m_x + 80, self.m_y + 110

    def collide(self, other, group):
        if group == "castle:eWar":
            self.collision = True
        if group == 'war:eWar':
            self.collision = True

    def take_damage(self, damage):
        EnemyWarrior.collision_sound_effect.play()
        self.health_point -= damage
        if self.health_point <= 0:
            self.die()

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

    def die(self):
        if self.health_point > 0:
            return BehaviorTree.FAIL

        if self.cur_state != DEAD:
            EnemyWarrior.dead_sound_effect.play()
            self.cur_state = DEAD
            self.frame = 0

        if self.frame >= 16:
            remove_object(self)
            remove_collision_object(self)
            return BehaviorTree.SUCCESS

        return BehaviorTree.RUNNING

    def run_to_left(self):
        if self.cur_state != RUN:
            self.cur_state = RUN
            self.dir_x = 1

        self.m_x -= self.dir_x * RUN_SPEED_PPS * game_framework.frame_time
        if self.cool_time > 0.0:
            self.cool_time -= game_framework.frame_time
        if self.m_x > 1150:
            self.m_x = 1150

        return BehaviorTree.SUCCESS

    def attack_enemy(self):
        if not self.collision:
            return BehaviorTree.FAIL

        if self.cur_state != HIT:
            EnemyWarrior.hit_sound_effect.play()
            self.cur_state = HIT
            self.dir_x = 0
            self.frame = 0
            self.do_hit = False

        if self.frame > 8 and not self.do_hit:
            for enemy in game_object[3]:
                if self.get_hit_bb()[0] < enemy.get_bounding_box()[2] and enemy.layer == self.layer:
                    enemy.take_damage(self.give_damage())
            for castle in game_object[1]:
                if self.get_hit_bb()[0] < castle.get_bounding_box()[2]:
                    castle.take_damage(self.give_damage())
            self.do_hit = True

        if int(self.frame) <= 3.0 and self.do_hit:
            self.cool_time = 2.5
            self.do_hit = False
            return BehaviorTree.SUCCESS

        return BehaviorTree.RUNNING

    def build_behavior_tree(self):
        check_cool_time_node = Leaf("Check Cool Time", self.check_cool_time)
        attack_enemy_node = Leaf("Attack Enemy", self.attack_enemy)
        attack_sequence = Sequence("Check Cool Time and Attack", check_cool_time_node, attack_enemy_node)

        run_node = Leaf("Run to Left", self.run_to_left)
        dead_node = Leaf("Dead", self.die)
        root_node = Selector("Attack or Run", dead_node, attack_sequence, run_node)
        self.bt = BehaviorTree(root_node)