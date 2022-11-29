from character import Character
import random
import game_framework

class NPC(Character):
    def __init__(self, i_x=0, i_y=0, i_attack=0, i_health=0, i_layer=1):
        self.pos_dif = random.randint(-20, 20)
        self.health_point = i_health
        self.dir_x = 1
        self.cool_time = 0.0
        self.layer = i_layer
        super().__init__(i_x + self.pos_dif, i_y + self.pos_dif, i_attack, 1)
        self.bt = None

    def update(self):
        self.bt.run()
        self.cur_state.do(self)
        if self.cool_time >= 0.0:
            self.cool_time -= game_framework.frame_time
        self.collision = False

    def draw(self):
        self.cur_state.draw(self)


