from pico2d import *
from npc import NPC
from game_world import game_object
from game_world import remove_object

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

        # self.frame_mouse = 0 # 기존 프레임 레이트에 맞추기 위한 마우스 프레임

    def idle(self): # +35, -20 스프라이트 오차 수정
        self.warrior_idle.clip_composite_draw(self.idle_size[0] * self.frame, 0, self.idle_size[0], self.idle_size[1],
                                              0, 'h', self.m_x + 35, self.m_y - 20, self.idle_size[0], self.idle_size[1])

    def hit(self): # +17, +15 스프라이트 오차 수정
        self.warrior_hit.clip_composite_draw(self.hit_size[0] * self.frame, 0, self.hit_size[0], self.hit_size[1],
                                             0, 'h', self.m_x + 17, self.m_y + 15, self.hit_size[0], self.hit_size[1])

    def run(self):
        self.warrior_run.clip_composite_draw(self.run_size[0] * self.frame, 0, self.run_size[0], self.run_size[1],
                                             0, 'h', self.m_x, self.m_y, self.run_size[0], self.run_size[1])

    def death(self):
        self.warrior_death.clip_composite_draw(self.death_size[0] * self.frame, 0, self.death_size[0], self.death_size[1],
                                             0, 'h', self.m_x, self.m_y, self.death_size[0], self.death_size[1])

    def update(self):
        self.frame_rate()
        if self.frame == 0 and self.state == -1:
            remove_object(self)
        self.hit_cool_time()
        self.move()
        if self.check_enemy() and self.state != -1:
            self.meet_enemy()

    def draw(self):
        if self.state == 0:
            self.idle()
        elif self.state == 1:
            self.run()
        elif self.state == 2:
            self.hit()
        elif self.state == -1:
            self.death()

    def frame_rate(self):
        if self.state == 0:  # idle
            self.frame = (self.frame + 1) % 8
            # 적이 없으면 상태 바꿔야함
            # if self.check_enemy == False:
            # elif self.cool_time == 0:
            #   self.state = 2
            #   self.frame = 0
            # if self.cool_time == 0: # 임시로 해둔 것
            #     self.state = 2
            #     self.frame = 0
        elif self.state == 1:  # run
            self.frame = (self.frame + 1) % 16
        elif self.state == 2:  # hit
            self.frame = (self.frame + 1) % 16
        elif self.state == -1:
            self.frame = (self.frame + 1) % 16

    def hit_cool_time(self):
        if self.frame == 0 and self.state == 2:
            self.state = 0
            self.cool_time = 100

        if self.cool_time != 0:
            self.cool_time -= 1
        elif self.cool_time == 0 and self.state == 0:
            self.state = 2
            self.frame = 0

    def move(self):
        if self.state != 1:
            return
        self.m_x += self.dir_x * 5
        if self.m_x > 1200:
            self.m_x = 1200

        # 만났을 때 실험
        # 원래는 히트 박스끼리 검사


    def check_enemy(self):
        # from play_state import e_warrior
        #
        #
        # if e_warrior == None:
        #      return False
        for enemy in game_object[1]:
            if self.m_x + 50 > enemy.m_x:
                return True
        return False

    def meet_enemy(self):
        if self.state == 2:
            return

        # 여기서 검사
        self.dir_x = 0
        if self.cool_time == 0:
            if self.frame != 0:
                self.frame = 0
            self.state = 2
        else:
            self.state = 0

