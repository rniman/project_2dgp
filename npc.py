
from character import  Character

class NPC(Character):
    def __init__(self, i_x=0, i_y=0, i_attack=0, i_health = 0):
        super().__init__(i_x, i_y, i_attack, 1)
        self.health_point = i_health
        self.dir_x = 1
        self.cool_time = 0