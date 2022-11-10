from pico2d import *
from npc import NPC
from game_world import game_object
from game_world import remove_object


class EnemyWarrior(NPC):
    warrior_idle = None
    warrior_run = None
    warrior_hit = None
    warrior_death = None
    idle_size = (120, 108)
    run_size = (123, 113)
    hit_size = (174, 136)
    death_size = (195, 149)
    def __init__(self):
        super().__init__(1200, 40, 10, 70)
        if EnemyWarrior.warrior_idle == None:
            self.warrior_idle = load_image('image/Ewarrior_idle.png')
            self.warrior_run = load_image('image/Ewarrior_run.png')
            self.warrior_hit = load_image('image/Ewarrior_hit.png')
            self.warrior_death = load_image('image/Ewarrior_death.png')

    def idle(self):
        self.warrior_idle.clip_draw_to_origin(self.idle_size[0] * self.frame, 0, self.idle_size[0], self.idle_size[1],
                                              self.m_x, self.m_y, self.idle_size[0], self.idle_size[1])

    def hit(self):
        self.warrior_hit.clip_draw_to_origin(self.hit_size[0] * self.frame, 0, self.hit_size[0], self.hit_size[1],
                                             self.m_x, self.m_y, self.hit_size[0], self.hit_size[1])

    def run(self):
        self.warrior_run.clip_draw_to_origin(self.run_size[0] * self.frame, 0, self.run_size[0], self.run_size[1],
                                            self.m_x, self.m_y, self.run_size[0], self.run_size[1])

    def death(self):
        self.warrior_death.clip_draw_to_origin(self.death_size[0] * self.frame, 0, self.death_size[0], self.death_size[1],
                                            self.m_x, self.m_y, self.death_size[0], self.death_size[1])

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
        if self.state == 0: # idle
            self.frame = (self.frame + 1) % 8
        elif self.state == 1: # run
            self.frame = (self.frame + 1) % 16
        elif self.state == 2: # hit
            self.frame = (self.frame + 1) % 12
        elif self.state == -1:
            self.frame = (self.frame + 1) % 16

    def move(self):
        if self.state != 1:
            return
        self.m_x -= self.dir_x * 5
        if self.m_x < 100:
            self.m_x = 100
            self.state = 2


    def hit_cool_time(self):
        if self.frame == 0 and self.state == 2:
            self.state = 0
            self.cool_time = 100

        if self.cool_time != 0:
            self.cool_time -= 1
        elif self.cool_time == 0 and self.state == 0:
            self.state = 2
            self.frame = 0

    def check_enemy(self):
        if self.state == -1:
            return
        #
        # from play_state import warrior

        for enemy in game_object[2]:
            if self.m_x - 50 < enemy.m_x:
                return True
        self.dir_x = 1
        self.state = 1
        return False

    def meet_enemy(self):
        if self.state == 2:
            return

        self.dir_x = 0
        if self.cool_time == 0:
            if self.frame != 0:
                self.frame = 0
            self.state = 2
        else:
            self.state = 0
