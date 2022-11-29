from pico2d import *
from character import Character
from warrior import Warrior
import game_world
import game_framework
import ladder

width = 1280
height = 720
bar_width = 1808
bar_height = 124
col_bar_width = 1730
col_bar_height = 66

SPACE, RD, LD, RU, LU, UD, DD, UU, DU, KEY1, KEY5, \
CHANGETOIDLE, CHANGETORUN= range(13)

key_event_table = {
    (SDL_KEYDOWN, SDLK_SPACE): SPACE,
    (SDL_KEYDOWN, SDLK_RIGHT): RD,
    (SDL_KEYDOWN, SDLK_LEFT): LD,
    (SDL_KEYDOWN, SDLK_UP): UD,
    (SDL_KEYDOWN, SDLK_DOWN): DD,
    (SDL_KEYDOWN, SDLK_1): KEY1,
    (SDL_KEYDOWN, SDLK_5): KEY5,
    (SDL_KEYUP, SDLK_RIGHT): RU,
    (SDL_KEYUP, SDLK_LEFT): LU,
    (SDL_KEYUP, SDLK_UP): UU,
    (SDL_KEYUP, SDLK_DOWN): DU
}

#RUN SPEED
PIXEL_PER_METER = 10.0 / 0.1 # 10픽셀당 10cm

RUN_SPEED_KMPH = 10.0
RUN_SPEED_MPH = RUN_SPEED_KMPH * 1000.0 / 60.0
RUN_SPEED_MPS = RUN_SPEED_MPH / 60.0
RUN_SPEED_PPS = RUN_SPEED_MPS * PIXEL_PER_METER

CLIMB_SPEED_KMPH = 5.0
CLIMB_SPEED_MPH = CLIMB_SPEED_KMPH * 1000.0 / 60.0
CLIMB_SPEED_MPS = CLIMB_SPEED_MPH / 60.0
CLIMB_SPEED_PPS = CLIMB_SPEED_MPS * PIXEL_PER_METER

TIME_PER_ACTION = 0.4
TIME_PER_HIT = 0.3
ACTION_PER_TIME = 1.0/TIME_PER_ACTION
HIT_PER_TIME = 1.0/TIME_PER_HIT
FRAMES_PER_ACTION = 8
FRAMES_PER_HIT = 12

class IDLE:
    @staticmethod
    def enter(self, event):
        if self.dir_x != None:
            self.dir_x = 0
        return True

    @staticmethod
    def exit(self, event):
        if event == KEY1:
            self.summon(event)
        elif event == KEY5:
            self.summon(event)

    @staticmethod
    def do(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8

    @staticmethod
    def draw(self):
        if self.look_at == 1:
            self.idle.clip_draw_to_origin(int(self.frame) * self.idle_size[0], 0,
                                          self.idle_size[0], self.idle_size[1],
                                          self.m_x, self.m_y)
        else:
            self.composite_idle.clip_draw_to_origin(int(self.frame) * self.idle_size[0], 0,
                                                    self.idle_size[0], self.idle_size[1],
                                                    self.m_x, self.m_y)

class RUN:
    @staticmethod
    def enter(self, event):
        if event == LD:
            if self.dir_x == None:
                self.dir_x = 0
            self.look_at = -1
            self.dir_x -= 1
        elif event == RU and self.dir_x != None:
            self.look_at = -1
            self.dir_x -= 1
        elif event == RD:
            if self.dir_x == None:
                self.dir_x = 0
            self.look_at = 1
            self.dir_x += 1
        elif event == LU and self.dir_x != None:
            self.look_at = 1
            self.dir_x += 1
        elif self.dir_x == None:
            self.dir_x = 0
            return False
        return True

    @staticmethod
    def exit(self, event):
        if event == KEY1:
            self.summon(event)
        elif event == KEY5:
            self.summon(event)

    @staticmethod
    def do(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        self.m_x += self.dir_x * RUN_SPEED_PPS * game_framework.frame_time
        self.m_x = clamp(40, self.m_x, 1160)

    @staticmethod
    def draw(self):
        if self.look_at == 1:
            self.run.clip_draw_to_origin(int(self.frame) * self.run_size[0], 0,
                                         self.run_size[0], self.run_size[1],
                                         self.m_x, self.m_y)
        else:
            self.composite_run.clip_draw_to_origin(int(self.frame) * self.run_size[0], 0,
                                                   self.run_size[0], self.run_size[1],
                                                   self.m_x, self.m_y)

class HIT:
    @staticmethod
    def enter(self, event):
        if event == SPACE and self.prev_state != HIT:
            self.frame = 0
            self.do_hit = False
        elif event == LD:
            if self.dir_x == None:
                self.dir_x = 0
            self.dir_x -= 1
        elif event == RU and self.dir_x != None:
            self.dir_x -= 1
        elif event == RD:
            if self.dir_x == None:
                self.dir_x = 0
            self.dir_x += 1
        elif event == LU and self.dir_x != None:
            self.dir_x += 1
        elif event == UU or event == DD:
            if self.dir_y != None:
                self.dir_y -= 1
        elif event == UD or event == DU:
            if self.dir_y != None:
                self.dir_y += 1

        return True

    @staticmethod
    def exit(self, event):
        if event == KEY1:
            self.summon(event)
        elif event == KEY5:
            self.summon(event)

    @staticmethod
    def do(self):
        oldFrame = self.frame
        self.frame = (self.frame + FRAMES_PER_HIT * HIT_PER_TIME * game_framework.frame_time) % 12

        if self.frame > 8 and self.do_hit == False:
            for enemy in game_world.game_object[2]:
                if self.get_hit_bb()[0] > enemy.get_bounding_box()[2]:
                    continue
                if self.get_hit_bb()[2] < enemy.get_bounding_box()[0]:
                    continue
                if self.get_hit_bb()[1] > enemy.get_bounding_box()[3]:
                    continue
                if self.get_hit_bb()[3] < enemy.get_bounding_box()[1]:
                    continue
                enemy.take_damage(self.give_damage())
            self.do_hit = True

        if int(oldFrame) >= 10 and int(self.frame) <= 3:
            self.hit_sound_effect.play()
            if self.dir_x == None:
                self.add_event(CHANGETOIDLE)
            elif self.dir_x == 0:
                if not self.event_que:  # 남아 있는 이벤트 없다면 그냥 이벤트 추가
                    self.add_event(CHANGETOIDLE)
                else:  # 남아있는 이벤트 조사
                    remain_event = 0
                    for event in self.event_que:
                        if event > 0 and event < 5:
                            remain_event += 1
                    if remain_event % 2 != 0:
                        self.add_event(CHANGETORUN)
                    else:
                        self.add_event(CHANGETOIDLE)
            else:
                if not self.event_que:
                    self.add_event(CHANGETORUN)
                    self.set_look()
                else:
                    remain_event = 0
                    for event in self.event_que:
                        if event > 0 and event < 5:
                            remain_event += 1
                    if remain_event % 2 != 0:
                        self.add_event(CHANGETOIDLE)
                    else:
                        self.add_event(CHANGETORUN)

    @staticmethod
    def draw(self):
        if self.look_at == 1:
            self.hit.clip_draw_to_origin(int(self.frame) * self.hit_size[0], 0,
                                         self.hit_size[0], self.hit_size[1],
                                         self.m_x - 10, self.m_y)
        elif self.look_at == -1:
            self.composite_hit.clip_draw_to_origin(int(self.frame) * self.hit_size[0], 0,
                                                   self.hit_size[0], self.hit_size[1],
                                                   self.m_x - 80, self.m_y)

class CLIMB:
    @staticmethod
    def enter(self, event):
        if event == UD:
            if self.dir_y == None:
                self.dir_y = 0
            self.dir_y += 1

            box = self.get_bounding_box()
            if box[0] > 335 and box[2] < 765:
                return False
            if box[2] < 265 or box[0] > 835:
                return False
            if box[1] != 40:
                return False

            if self.m_y == 40:
                self.m_y += 5
                if self.m_x < 500:
                    self.m_x = 220
                else:
                    self.m_x = 720

        elif event == DD:
            if self.dir_y == None:
                self.dir_y = 0
            self.dir_y -= 1

            box = self.get_bounding_box()
            if box[0] > 335 and box[2] < 765:
                return False
            if box[2] < 265 or box[0] > 835:
                return False
            if box[1] != 245:
                return False

            if self.m_y == 245:
                self.m_y -= 5
                if self.m_x < 500:
                    self.m_x = 220
                else:
                    self.m_x = 720

        elif event == UU and self.dir_y != None:
            self.dir_y -= 1
            if self.prev_state == CLIMB:
                pass
            else:
                return False

        elif event == DU and self.dir_y != None:
            self.dir_y += 1
            if self.prev_state == CLIMB:
                pass
            else:
                return False

        elif event == UU or event == DU:
            self.dir_y = 0
            return False

        elif event == LD or event == RU:
            self.dir_x -= 1
        elif event == RD or event == LU:
            self.dir_x += 1

        return True

    @staticmethod
    def exit(self, event):
        if event == KEY1:
            self.summon(event)
        elif event == KEY5:
            self.summon(event)

    @staticmethod
    def do(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        self.m_y += self.dir_y * CLIMB_SPEED_PPS * game_framework.frame_time
        if self.m_y > 245:
            self.m_y = 245
            if self.look_at == -1:
                self.m_x += 40  # flip x좌표 이미지 보정

            if self.dir_x == 0:
                self.add_event(CHANGETOIDLE)
            else:
                self.set_look()
                self.add_event(CHANGETORUN)

        elif self.m_y < 40:
            self.m_y = 40
            if self.look_at == -1:
                self.m_x += 40  # flip x좌표 이미지 보정

            if self.dir_x == 0:
                self.add_event(CHANGETOIDLE)
            else:
                self.add_event(CHANGETORUN)
                self.set_look()

    @staticmethod
    def draw(self):
        self.climb.clip_draw_to_origin(int(self.frame) * self.climb_size[0], 0,
                                       self.climb_size[0], self.climb_size[1],
                                       self.m_x, self.m_y)

next_state = {
    IDLE: {SPACE: HIT, LD: RUN, LU: RUN, RD: RUN, RU: RUN, UD: CLIMB, DD: CLIMB, UU: CLIMB, DU: CLIMB, KEY1: IDLE,
           KEY5: IDLE, CHANGETOIDLE: IDLE, CHANGETORUN: RUN},
    RUN: {SPACE: HIT, LD: IDLE, LU: IDLE, RD: IDLE, RU: IDLE, UD: CLIMB, DD: CLIMB, UU: CLIMB, DU: CLIMB, KEY1: RUN,
          KEY5: RUN, CHANGETOIDLE: IDLE, CHANGETORUN: RUN},
    HIT: {SPACE: HIT, LD: HIT, LU: HIT, RD: HIT, RU: HIT, UD: HIT, DD: HIT, UU: HIT, DU: HIT, KEY1: HIT,
          KEY5: HIT, CHANGETOIDLE: IDLE, CHANGETORUN: RUN},
    CLIMB: {SPACE: CLIMB, LD: CLIMB, LU: CLIMB, RD: CLIMB, RU: CLIMB, UD: CLIMB, DD: CLIMB, UU: CLIMB, DU: CLIMB,
            KEY1: CLIMB,  KEY5: CLIMB, CHANGETOIDLE: IDLE, CHANGETORUN: RUN}
}


# 1층 y좌표 40, 2층 y좌표 250
# 10km/h의 이동속도
# 자원은 초당 1씩오르며 최대 10까지 보관가능
#
# 바운딩 박스
# if self.cur_state == CLIMB:
#    self.m_x + 50, self.m_y, self.m_x + 110, self.m_y + 100
# if self.look_at == 1:
#    return self.m_x + 50, self.m_y, self.m_x + 120, self.m_y + 100
# else:
#    return self.m_x, self.m_y, self.m_x + 70, self.m_y + 100
# 히트 사이즈 70
class MainCharacter(Character):
    def __init__(self):
        super().__init__(50, 40, 10)
        self.idle = load_image('image/main_idle.png')
        self.run = load_image('image/main_run.png')
        self.hit = load_image('image/main_hit.png')
        self.climb = load_image('image/main_climb.png')
        self.composite_idle = load_image('image/main_idle_composite.png')
        self.composite_run = load_image('image/main_run_composite.png')
        self.composite_hit = load_image('image/main_hit_composite.png')

        self.resource_bar = load_image('image/bar.png')
        self.resource = load_image('image/resource.png')

        self.hit_sound_effect = load_wav('sound_effect/main_swing.wav')

        self.idle_size = (124, 95)
        self.run_size = (143, 110)
        self.climb_size = (125, 87)
        self.hit_size = (216, 168)

        self.now_resource = 3.0
        self.max_resource = 10.0

        self.dir_x = None
        self.dir_y = None
        self.look_at = 1
        self.can_climb = False

        self.event_que = []
        self.cur_state = IDLE
        self.prev_state = None
        self.cur_state.enter(self, None)

    def add_event(self, event):
        self.event_que.insert(0, event)

    def handle_event(mainChar, event):
        if(event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            mainChar.add_event(key_event)

    def update(self):
        self.get_now_resource()
        # 이벤트 큐가 있다면 이벤트 발생
        self.cur_state.do(self)
        if self.event_que:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.prev_state = self.cur_state
            self.cur_state = next_state[self.cur_state][event]
            if self.cur_state.enter(self, event) != True:
                self.cur_state = self.prev_state


    def draw(self):
        #
        self.resource_bar.clip_draw_to_origin(0, 0, bar_width, bar_height, width // 2 - 301, 640,
                                              bar_width // 3, bar_height // 3)
        # 13, 10은 테두리 맞춰줌
        self.resource.clip_draw_to_origin(0, 0,
                                          int(col_bar_width * self.now_resource // self.max_resource), col_bar_height,
                                          width // 2 + 13 - 301, 640 + 10,
                                          int(col_bar_width // 3 * self.now_resource // self.max_resource),
                                          col_bar_height // 3)
        self.cur_state.draw(self)
        draw_rectangle(*self.get_bounding_box())

    def get_now_resource(self):
        if self.now_resource < 10.0:
            self.now_resource += game_framework.frame_time

    def set_look(self):
        if self.dir_x == 1:
            self.look_at = 1
        elif self.dir_x == -1:
            self.look_at = -1

    # 자원 3을 소비하여 소환
    def summon(self, event):
        if event == KEY1 and self.now_resource >= 3.0:
            self.now_resource -= 3.0
            warrior = Warrior(1)
            game_world.add_object(warrior, 3)
            game_world.add_collision_pairs(warrior, None, 'war:eWar')
        elif event == KEY5 and self.now_resource >= 3.0:
            self.now_resource -= 3.0
            warrior = Warrior(2)
            game_world.add_object(warrior, 3)
            game_world.add_collision_pairs(warrior, None, 'war:eWar')

    def get_bounding_box(self):
        if self.cur_state == CLIMB:
            return self.m_x + 50, self.m_y, self.m_x + 110, self.m_y + 100
        if self.look_at == 1:
            return self.m_x + 50, self.m_y, self.m_x + 120, self.m_y + 100
        else:
            return self.m_x, self.m_y, self.m_x + 70, self.m_y + 100

    def get_hit_bb(self):
        if self.look_at == 1:
            return self.m_x + 120, self.m_y, self.m_x + 190, self.m_y + 100
        else:
            return self.m_x - 70, self.m_y, self.m_x, self.m_y + 100

    def collide(self, other, group):
        pass

    def no_collide(self, other, group):
        pass

    def take_damage(self, damage):
        pass

