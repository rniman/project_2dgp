from pico2d import *
import game_framework
import logo_state

width = 1280
height = 720
bar_width = 1808
bar_height = 124
col_bar_width = 1730
col_bar_height = 66

class Castle:
    def __init__(self):
        self.castle = load_image("image/castle.png")
        self.hp_bar = load_image("image/bar.png")
        self.hp = load_image("image/hp2.png")
        self.m_x = 0
        self.m_y = 245
        self.max_hp = 1000
        self.now_hp = 1000

    def draw(self):
        self.castle.draw(self.m_x, self.m_y)
        self.hp_bar.clip_draw_to_origin(0, 0, bar_width, bar_height, width//2 - 301, 680,
                                        bar_width // 3, bar_height // 3)
        self.hp.clip_draw_to_origin(0, 0, col_bar_width  * self.now_hp // self.max_hp, col_bar_height, width//2 + 13 - 301, 680 + 10,
                                    col_bar_width // 3  * self.now_hp // self.max_hp, col_bar_height // 3)

class BackGround:
    def __init__(self):
        self.backGround = load_image('image/Bground.png')

    def draw(self):
        self.backGround.draw(width // 2, height // 2)

class Floor:
    def __init__(self):
        self.floor = load_image('image/tile.png')
        self.tile_width = 90

    def draw(self):
        for x in range(98, width, self.tile_width):
            self.floor.draw(x, 245)
            x = x + self.tile_width

class Ladder:
    def __init__(self):
        self.ladder = load_image('image/ladder.png')
        self.mx = (300, 800)

    def draw(self):
        self.ladder.draw(self.mx[0], 160)
        self.ladder.draw(self.mx[1], 160)

class Character:
    def __init__(self, i_x=0, i_y=0, i_attack=0, i_state=0):
        self.state = i_state
        self.frame = 0
        self.m_x = i_x
        self.m_y = i_y
        self.dir_x = 0
        self.attack_damage = i_attack


class MainCharacter(Character):

    def __init__(self):
        super().__init__(100, 90, 10)
        self.main_idle = load_image('image/main_idle.png')
        self.main_run = load_image('image/main_run.png')
        self.main_hit = load_image('image/main_hit.png')
        self.main_climb = load_image('image/main_climb.png')
        self.resource_bar = load_image('image/bar.png')
        self.resource = load_image('image/resource.png')
        self.idle_size = (373, 286)
        self.run_size = (428, 331)
        self.climb_size = (376, 262)
        self.hit_size = (647, 504)
        self.box = [self.m_x, self.m_y, self.m_x + self.idle_size[0]//6, self.m_y + self.idle_size[1]//3]
        self.now_resource = 0
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

    def idle(self):
        self.main_idle.clip_draw(0 + self.frame * self.idle_size[0], 0, self.idle_size[0], self.idle_size[1],
                                 self.m_x, self.m_y, self.idle_size[0] // 3, self.idle_size[1] // 3)

    def flip_idle(self):
        self.main_idle.clip_composite_draw(0 + self.frame * self.idle_size[0], 0, self.idle_size[0], self.idle_size[1],
                                           0, 'h', self.m_x, self.m_y, self.idle_size[0] // 3, self.idle_size[1] // 3)

    def run(self):
        self.main_run.clip_draw(0 + self.frame * self.run_size[0], 0, self.run_size[0], self.run_size[1],
                                self.m_x, self.m_y, self.run_size[0] // 3, self.run_size[1] // 3)

    def flip_run(self):
        self.main_run.clip_composite_draw(0 + self.frame * self.run_size[0], 0, self.run_size[0], self.run_size[1],
                                          0, 'h', self.m_x, self.m_y, self.run_size[0] // 3, self.run_size[1] // 3)

    def climb(self):
        self.main_climb.clip_draw(0 + self.frame * self.climb_size[0], 0, self.climb_size[0], self.climb_size[1],
                                  self.m_x, self.m_y, self.climb_size[0] // 3, self.climb_size[1] // 3)

    def hit(self):  # y, 120
        self.main_hit.clip_draw(0 + self.frame * self.hit_size[0], 0, self.hit_size[0], self.hit_size[1],
                                self.m_x, self.m_y + 20, self.hit_size[0] // 3, self.hit_size[1] // 3)

    def flip_hit(self):  # y, 120
        self.main_hit.clip_composite_draw(0 + self.frame * self.hit_size[0], 0, self.hit_size[0], self.hit_size[1],
                                          0, 'h', self.m_x, self.m_y + 20, self.hit_size[0] // 3, self.hit_size[1] // 3)

    def update(self):
        self.frame_rate()
        self.move()
        self.get_now_resource()

    def draw(self):
        #
        self.resource_bar.clip_draw_to_origin(0, 0, bar_width, bar_height, width // 2 - 301, 640,
                                              bar_width // 3, bar_height // 3)
        # 13, 10은 테두리 맞춰줌
        self.resource.clip_draw_to_origin(0, 0, col_bar_width * self.now_resource // self.max_resource, col_bar_height,  width // 2 + 13 - 301, 640 + 10,
                                          col_bar_width // 3  * self.now_resource // self.max_resource, col_bar_height // 3)

        if self.state == 0 and self.look_at == 1:
            self.idle()
        elif self.state == 0 and self.look_at == -1:
            self.flip_idle()
        elif self.state == 1 and self.look_at == 1:
            self.run()
        elif self.state == 1 and self.look_at == -1:
            self.flip_run()
        elif self.state == 2:
            self.climb()
        elif self.state == 3 and self.look_at == 1:
            self.hit()
        elif self.state == 3 and self.look_at == -1:
            self.flip_hit()

    def frame_rate(self):
        if self.state == 0:
            self.frame = (self.frame + 1) % 8
        elif self.state == 1:
            self.frame = (self.frame + 1) % 8
        elif self.state == 2:
            self.frame = (self.frame + 1) % 8
        elif self.state == 3:
            self.frame = (self.frame + 1) % 12
            if self.frame == 0:
                if self.dir_x == 0:
                    self.state = 0
                else:
                    self.state = 1

    def set_box(self):
        if self.look_at == 1:
            self.box = [self.m_x, self.m_y, self.m_x + self.idle_size[0] // 6, self.m_y + self.idle_size[1] // 3]
        else:
            self.box = [self.m_x - self.idle_size[0] // 6, self.m_y, self.m_x, self.m_y - self.idle_size[1] // 3]

    def move(self):
        if self.state == 1 or self.state == 0:
            self.m_x += self.dir_x * 5
            if self.m_x > 1200:
                self.m_x = 1200
            elif self.m_x < 100:
                self.m_x = 100
            self.set_box()
        elif self.state == 2:
            self.ladder_move()

    def ladder_move(self):
        self.m_y += self.dir_y * 5
        if self.m_y > 300:
            self.m_y = 300
            if self.dir_x == 0:
                self.state = 0
            else:
                self.state = 1
            if self.look_at == -1:
                self.m_x += 35  # flip x좌표 이미지 보정
        elif self.m_y < 90:
            if self.dir_x == 0:
                self.state = 0
            else:
                self.state = 1
            self.m_y = 90
            if self.look_at == -1:
                self.m_x += 35  # flip x좌표 이미지 보정

    def get_now_resource(self):
        if self.now_resource < 300:
            self.now_resource += 1

class NonePlayableCharacter(Character):
    def __init__(self, i_x=0, i_y=0, i_attack=0, i_health = 0):
        super().__init__(i_x, i_y, i_attack, 1)
        self.health_point = i_health
        self.dir_x = 1
        self.cool_time = 0

class WarriorCharacter(NonePlayableCharacter):

    def __init__(self, i_key):
        # 1층 115  2층 325
        if i_key == 1:
            super().__init__(90, 115, 5, 50)
        elif i_key == 5:
            super().__init__(90, 325, 5, 50)
        self.warrior_idle = load_image('image/warrior_idle.png')
        self.warrior_run = load_image('image/warrior_run.png')
        self.warrior_hit = load_image('image/warrior_hit.png')
        self.warrior_death = load_image('image/warrior_death.png')
        self.idle_size = (121, 106)
        self.run_size = (131, 158)
        self.hit_size = (198, 175)
        self.death_size = (187, 175)
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
        self.hit_cool_time()
        self.move()

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
            if self.frame == 0:
                self.delete_self()

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
        # if self.check_enemy(enemy):
        if self.m_x >= 500:
            self.meet_enemy()

    def check_enemy(self, enemy_list):
        for enemy in enemy_list:
            if self.m_x + 50 > enemy.m_x:
                return True
        return False

    def meet_enemy(self):
        # 여기서 검사
        self.dir_x = 0
        if self.cool_time == 0:
            if self.frame != 0:
                self.frame = 0
            self.state = 2
        else:
            self.state = 0

    def delete_self(self):
        warrior.remove(self)

class EnemyWarriorCharacter(NonePlayableCharacter):
    def __init__(self):
        super().__init__(1200, 90, 10, 70)
        self.warrior_idle = load_image('image/Ewarrior_idle.png')
        self.warrior_run = load_image('image/Ewarrior_run.png')
        self.warrior_hit = load_image('image/Ewarrior_hit.png')
        # self.warrior_death = load_image('image/Ewarrior_death.png')
        self.idle_size = (113, 108)
        self.run_size = (122, 113)
        self.hit_size = (174, 136)
        # self.death_size = (187, 175)

    def idle(self):
        self.warrior_idle.clip_composite_draw(self.idle_size[0] * self.frame, 0, self.idle_size[0], self.idle_size[1],
                                              0, 'h', self.m_x + 35, self.m_y - 20, self.idle_size[0], self.idle_size[1])

    def hit(self):
        self.warrior_hit.clip_composite_draw(self.hit_size[0] * self.frame, 0, self.hit_size[0], self.hit_size[1],
                                             0, 'h', self.m_x + 17, self.m_y + 15, self.hit_size[0], self.hit_size[1])

    def run(self):
        self.warrior_run.clip_composite_draw(self.run_size[0] * self.frame, 0, self.run_size[0], self.run_size[1],
                                             0, 'h', self.m_x, self.m_y, self.run_size[0], self.run_size[1])

    # def death(self):
    #     self.warrior_death.clip_composite_draw(self.death_size[0] * self.frame, 0, self.death_size[0], self.death_size[1],
    #                                          0, 'h', self.m_x, self.m_y, self.death_size[0], self.death_size[1])

    def update(self):
        pass

    def draw(self):
        if self.state == 0:
            self.idle()
        elif self.state == 1:
            self.run()
        elif self.state == 2:
            self.hit()
        # elif self.state == -1:
        #     self.death()


    def frame_rate(self):
        if self.state == 0:
            self.frame = (self.frame + 1) % 8
        elif self.state == 1:
            self.frame = (self.frame + 1) % 16
        elif self.state == 2:
            self.frame = (self.frame + 1) % 12

    def move(self):
        pass

    def hit_cool_time(self):
        pass

    def check_enenmy(self):
        pass

    def meet_enenmy(self):
        pass

    def delete_self(self):
        pass

def handle_events():
    global user
    global warrior
    events = get_events()
    for event in events:
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
            elif event.key == SDLK_q:
                for war in warrior:
                    war.state = -1
            elif event.key == SDLK_UP:
                user.dir_y += 1
                if (user.box[0] > 300 - 70 and user.box[2] < 300 + 70):
                    if user.m_y == 90:
                        user.state = 2
                        user.m_x = 280
                        user.m_y += 5
                elif (user.box[0] > 800 - 70 and user.box[2] < 800 + 70):
                    if user.m_y == 90:
                        user.state = 2
                        user.m_x = 780
                        user.m_y += 5
            elif event.key == SDLK_DOWN:
                user.dir_y -= 1
                if (user.box[0] > 300 - 70 and user.box[2] < 300 + 70):
                    if user.m_y == 300:
                        user.state = 2
                        user.m_x = 280
                        user.m_y -= 5
                elif (user.box[0] > 800 - 70 and user.box[2] < 800 + 70):
                    if user.m_y == 300:
                        user.state = 2
                        user.m_x = 780
                        user.m_y -= 5
            elif event.key == SDLK_RIGHT:
                if user.state != 2:
                    user.state = 1
                user.dir_x += 1
                if user.dir_x == 0 and user.state != 2:
                    user.state = 0
            elif event.key == SDLK_LEFT:
                if user.state != 2:
                    user.state = 1
                user.dir_x -= 1
                if user.dir_x == 0 and user.state != 2:
                    user.state = 0
            elif event.key == SDLK_SPACE and user.state != 2:
                user.frame = 0
                user.state = 3
            elif event.key == SDLK_1 and user.now_resource >= 100:
                user.now_resource -= 100
                warrior.append(WarriorCharacter(1))
            elif event.key == SDLK_5 and user.now_resource >= 100:
                user.now_resource -= 100
                warrior.append(WarriorCharacter(5))

        elif event.type == SDL_KEYUP:
            if event.key == SDLK_UP:
                user.dir_y -= 1
            elif event.key == SDLK_DOWN:
                user.dir_y += 1
            elif event.key == SDLK_RIGHT:
                user.dir_x -= 1
                if user.dir_x == 0 and user.state != 2:
                    user.state = 0
                elif user.state != 2:
                    user.state = 1
            elif event.key == SDLK_LEFT:
                user.dir_x += 1
                if user.dir_x == 0 and user.state != 2:
                    user.state = 0
                elif user.state != 2:
                    user.state = 1

        if user.dir_x > 0:
            user.look_at = 1
        elif user.dir_x < 0:
            user.look_at = -1


back_ground = None
ladder = None
floor = None
castle = None
user = None
warrior = None
e_warrior = None
time = 0

# 초기화
def enter():
    global back_ground, ladder, floor
    global castle
    global user, warrior
    back_ground = BackGround()
    ladder = Ladder()
    floor = Floor()
    warrior = []
    castle = Castle()
    user = MainCharacter()
# 종료
def exit():
    del back_ground
    del ladder
    del floor
    del warrior
    del user
    del castle

# 월드의 존재하는 객체들을 업데이트
def update():
    for w in warrior:
        w.update()
    user.update()
    delay(0.03)

# 월드를 그린다
def draw():
    clear_canvas()
    back_ground.draw()
    castle.draw()
    floor.draw()
    ladder.draw()
    for w in warrior:
        w.draw()
    user.draw()
    update_canvas()




