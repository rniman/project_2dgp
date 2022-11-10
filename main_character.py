import logo_state
from pico2d import *
from character import Character
from warrior import Warrior
import game_world

width = 1280
height = 720
bar_width = 1808
bar_height = 124
col_bar_width = 1730
col_bar_height = 66

SPACE, RD, LD, RU, LU, UD, DD, UU, DU, KEY1, KEY5 = range(11)

key_event_table = {
    (SDL_KEYDOWN, SDLK_SPACE) : SPACE,
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


class IDLE:
    @staticmethod
    def enter(self, event):
        self.dir_x = 0
        # self.dir_y = 0
        pass

    @staticmethod
    def exit(self, event):
        if event == KEY1:
            self.summon(event)
        elif event == KEY5:
            self.summon(event)
        else:
            self.frame = 0

    @staticmethod
    def do(self):
        self.frame = (self.frame + 1) % 8

    @staticmethod
    def draw(self):
        if self.look_at == 1:
            self.main_idle.clip_draw(0 + self.frame * self.idle_size[0], 0, self.idle_size[0], self.idle_size[1],
                                     self.m_x, self.m_y, self.idle_size[0], self.idle_size[1])
        else:
            self.main_idle.clip_composite_draw(0 + self.frame * self.idle_size[0], 0,
                                               self.idle_size[0], self.idle_size[1],
                                               0, 'h', self.m_x, self.m_y, self.idle_size[0], self.idle_size[1])

class RUN:
    @staticmethod
    def enter(self, event):
        if event == LD or event == RU:
            self.look_at = -1
            self.dir_x -= 1
        elif event == RD or event == LU:
            self.look_at = 1
            self.dir_x += 1


    @staticmethod
    def exit(self, event):
        if event == KEY1:
            self.summon(event)
        elif event == KEY5:
            self.summon(event)
        else:
            self.frame = 0

    @staticmethod
    def do(self):
        self.frame = (self.frame + 1) % 8

        self.m_x += self.dir_x * 5
        if self.m_x > 1200:
            self.m_x = 1200
        elif self.m_x < 100:
            self.m_x = 100
        self.set_box()

    @staticmethod
    def draw(self):
        if self.look_at == 1:
            self.main_run.clip_draw(0 + self.frame * self.run_size[0], 0, self.run_size[0], self.run_size[1],
                                    self.m_x, self.m_y, self.run_size[0], self.run_size[1])
        else:
            self.main_run.clip_composite_draw(0 + self.frame * self.run_size[0], 0,
                                              self.run_size[0], self.run_size[1],
                                              0, 'h', self.m_x, self.m_y, self.run_size[0], self.run_size[1])

class HIT:
    @staticmethod
    def enter(self, event):
        if event == SPACE and self.prev_state != HIT:
            self.frame = 0
        elif event == LD or event == RU:
            self.dir_x -= 1
        elif event == RD or event == LU:
            self.dir_x += 1
        elif event == UU or event == DD:
            self.dir_y -= 1
        elif event == UD or event == DU:
            self.dir_y += 1

    @staticmethod
    def exit(self, event):
        if event == KEY1:
            self.summon(event)
        elif event == KEY5:
            self.summon(event)

    @staticmethod
    def do(self):
        self.frame = (self.frame + 1) % 12
        if self.frame == 0:
            if self.dir_x == 0:
                self.change_state(IDLE, HIT)
                self.set_look()
            else:
                self.change_state(RUN, HIT)
                self.set_look()

    @staticmethod
    def draw(self):
        if self.look_at == 1:
            self.main_hit.clip_draw(0 + self.frame * self.hit_size[0], 0, self.hit_size[0], self.hit_size[1],
                                    self.m_x, self.m_y + 20, self.hit_size[0], self.hit_size[1])
        elif self.look_at == -1:
            self.main_hit.clip_composite_draw(0 + self.frame * self.hit_size[0], 0,
                                              self.hit_size[0], self.hit_size[1],
                                              0, 'h', self.m_x, self.m_y + 20, self.hit_size[0], self.hit_size[1])

class CLIMB:
    @staticmethod
    def enter(self, event):
        if event == UD:
            self.dir_y += 1
            if self.box[0] > 300 - 70 and self.box[2] < 300 + 70 and self.m_y == 90:
                self.m_x = 280
                self.m_y += 5
            elif self.box[0] > 800 - 70 and self.box[2] < 800 + 70 and self.m_y == 90:
                self.m_x = 780
                self.m_y += 5
            else:
                self.change_state(self.prev_state)

        elif event == DD:
            self.dir_y -= 1
            print(self.dir_y)
            if self.box[0] > 300 - 70 and self.box[2] < 300 + 70 and self.m_y == 300:
                self.m_x = 280
                self.m_y -= 5
            elif self.box[0] > 800 - 70 and self.box[2] < 800 + 70 and self.m_y == 300:
                self.m_x = 780
                self.m_y -= 5
            else:
                self.change_state(self.prev_state)

        elif event == UU:
            self.dir_y -= 1
            if self.prev_state == CLIMB:
                pass
            else:
                self.change_state(self.prev_state)

        elif event == DU:
            self.dir_y += 1
            print(self.dir_y)
            if self.prev_state == CLIMB:
                pass
            else:
                self.change_state(self.prev_state)

        elif event == LD or event == RU:
            self.dir_x -= 1
        elif event == RD or event == LU:
            self.dir_x += 1

    @staticmethod
    def exit(self, event):
        self.frame = 0
        if event == KEY1:
            self.summon(event)
        elif event == KEY5:
            self.summon(event)

    @staticmethod
    def do(self):
        self.frame = (self.frame + 1) % 8
        self.m_y += self.dir_y * 5
        if self.m_y > 300:
            self.m_y = 300
            if self.dir_x == 0:
                self.change_state(IDLE, CLIMB)
                self.set_look()
            else:
                self.change_state(RUN, CLIMB)
                self.set_look()

            if self.look_at == -1:
                self.m_x += 35  # flip x좌표 이미지 보정
        elif self.m_y < 90:
            if self.dir_x == 0:
                self.change_state(IDLE, CLIMB)
                self.set_look()

            else:
                self.change_state(RUN, CLIMB)
                self.set_look()

            self.m_y = 90
            if self.look_at == -1:
                self.m_x += 35  # flip x좌표 이미지 보정

    @staticmethod
    def draw(self):
        self.main_climb.clip_draw(0 + self.frame * self.climb_size[0], 0, self.climb_size[0], self.climb_size[1],
                                  self.m_x, self.m_y, self.climb_size[0], self.climb_size[1])

next_state = {
    IDLE: {SPACE: HIT, LD: RUN, LU: RUN, RD: RUN, RU: RUN, UD: CLIMB, DD: CLIMB, UU: CLIMB, DU: CLIMB, KEY1: IDLE,  KEY5: IDLE},
    RUN: {SPACE: HIT, LD: IDLE, LU: IDLE, RD: IDLE, RU: IDLE, UD: CLIMB, DD: CLIMB, UU: CLIMB, DU: CLIMB, KEY1: RUN,  KEY5: RUN},
    HIT: {SPACE: HIT, LD: HIT, LU: HIT, RD: HIT, RU: HIT, UD: HIT, DD: HIT, UU: HIT, DU: HIT, KEY1: HIT,  KEY5: HIT},
    CLIMB: {SPACE: CLIMB, LD: CLIMB, LU: CLIMB, RD: CLIMB, RU: CLIMB, UD: CLIMB, DD: CLIMB, UU: CLIMB, DU: CLIMB, KEY1: CLIMB,  KEY5: CLIMB}
}

class MainCharacter(Character):
    def __init__(self):
        super().__init__(100, 90, 10)
        self.main_idle = load_image('image/main_idle.png')
        self.main_run = load_image('image/main_run.png')
        self.main_hit = load_image('image/main_hit.png')
        self.main_climb = load_image('image/main_climb.png')
        self.resource_bar = load_image('image/bar.png')
        self.resource = load_image('image/resource.png')
        self.idle_size = (124, 95)
        self.run_size = (143, 110)
        self.climb_size = (125, 87)
        self.hit_size = (215, 168)
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

        self.event_que = []
        self.cur_state = IDLE
        self.prev_state = None
        self.cur_state.enter(self, None)

    def add_event(self, event):
        self.event_que.insert(0, event)

    def change_state(self, next_state, prev_state = None):
        self.cur_state.exit(self, None)
        self.cur_state = next_state
        if prev_state != None:
            self.prev_state = prev_state
        self.cur_state.enter(self, None)

    def handle_event(mainChar, event):
        if(event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            mainChar.add_event(key_event)

    def update(self):
        self.get_now_resource()
        self.cur_state.do(self)
        # 이벤트 큐가 있다면 이벤트 발생
        if self.event_que:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.prev_state = self.cur_state
            self.cur_state = next_state[self.cur_state][event]
            self.cur_state.enter(self, event)

    def draw(self):
        #
        self.resource_bar.clip_draw_to_origin(0, 0, bar_width, bar_height, width // 2 - 301, 640,
                                              bar_width // 3, bar_height // 3)
        # 13, 10은 테두리 맞춰줌
        self.resource.clip_draw_to_origin(0, 0, col_bar_width * self.now_resource // self.max_resource, col_bar_height,
                                          width // 2 + 13 - 301, 640 + 10,
                                          col_bar_width // 3  * self.now_resource // self.max_resource,
                                          col_bar_height // 3)
        self.cur_state.draw(self)

    def set_box(self):
        if self.look_at == 1:
            self.box = [self.m_x, self.m_y, self.m_x + self.idle_size[0] // 6, self.m_y + self.idle_size[1] // 3]
        else:
            self.box = [self.m_x - self.idle_size[0] // 6, self.m_y, self.m_x, self.m_y - self.idle_size[1] // 3]

    def get_now_resource(self):
        if self.now_resource < 300:
            self.now_resource += 1

    def set_look(self):
        if self.dir_x == 1:
            self.look_at = 1
        elif self.dir_x == -1:
            self.look_at = - 1

    def summon(self, event):
        if event == KEY1 and self.now_resource >= 100:
            self.now_resource -= 100
            warrior = Warrior(1)
            game_world.add_object(warrior, 2)
        elif event == KEY5 and self.now_resource >= 100:
            self.now_resource -= 100
            warrior = Warrior(5)
            game_world.add_object(warrior, 2)

