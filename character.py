PIXEL_PER_METER = 10.0 / 0.1  # 10픽셀당 10cm

class Character:
    def __init__(self, i_x=0, i_y=0, i_attack=0, i_state=0):
        self.state = i_state
        self.frame = 0
        self.m_x = i_x
        self.m_y = i_y
        self.dir_x = 1
        self.attack_damage = i_attack
        self.do_hit = False
        self.collision = False

    def give_damage(self):
        return self.attack_damage



