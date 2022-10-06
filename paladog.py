from pico2d import *

width = 1280
height = 720

tile_width = 90

open_canvas(width, height)

backGround = load_image('image/Bground.png')
Grass = load_image('image/Grass.png')
floor = load_image('image/tile.png')
ladder = load_image('image/ladder.png')

main_idle = load_image('image/main_idle.png')
main_run = load_image('image/main_run.png')
main_hit = load_image('image/main_hit.png')
main_cilmb = load_image('image/main_climb.png')

warrior_idle = load_image('image/warrior_idle.png')
warrior_run = load_image('image/warrior_run.png')
warrior_hit = load_image('image/warrior_hit.png')


class Character:
    def __init__(self, i_x=0, i_y=0, i_attack=0):
        self.state = 0
        self.frame = 0
        self.m_x = i_x
        self.m_y = i_y
        self.dir_x = 0
        self.attack_damage = i_attack


class MainCharacter(Character):
    def __init__(self):
        super().__init__(100, 90, 10)
        self.idle_size = (373, 286)
        self.run_size = (428, 331)
        self.climb_size = (376, 262)
        self.hit_size = (647, 504)
        self.box = []
        self.dir_x = 0
        self.dir_y = 0
        self.look_at = 1
        self.box = [self.m_x, self.m_y, self.m_x + self.idle_size[0]//6, self.m_y + self.idle_size[1]//3]

    def idle(self):
        main_idle.clip_draw(0 + self.frame * self.idle_size[0], 0, self.idle_size[0], self.idle_size[1], self.m_x, self.m_y,
                            self.idle_size[0] // 3, self.idle_size[1] // 3)

    def flip_idle(self):
        main_idle.clip_composite_draw(0 + self.frame * self.idle_size[0], 0, self.idle_size[0], self.idle_size[1], 0, 'h',
                                      self.m_x, self.m_y, self.idle_size[0] // 3, self.idle_size[1] // 3)

    def run(self):
        main_run.clip_draw(0 + self.frame * self.run_size[0], 0, self.run_size[0], self.run_size[1],
                           self.m_x, self.m_y, self.run_size[0] // 3, self.run_size[1] // 3)

    def flip_run(self):
        main_run.clip_composite_draw(0 + self.frame * self.run_size[0], 0, self.run_size[0], self.run_size[1],  0, 'h',
                                     self.m_x, self.m_y, self.run_size[0] // 3, self.run_size[1] // 3)

    def climb(self):
        main_cilmb.clip_draw(0 + self.frame * self.climb_size[0], 0, self.climb_size[0], self.climb_size[1],
                             self.m_x, self.m_y, self.climb_size[0] // 3, self.climb_size[1] // 3)

    def hit(self):  # y, 120
        main_hit.clip_draw(0 + self.frame * self.hit_size[0], 0, self.hit_size[0], self.hit_size[1],
                           self.m_x, self.m_y + 20, self.hit_size[0] // 3, self.hit_size[1] // 3)

    def flip_hit(self):  # y, 120
        main_hit.clip_composite_draw(0 + self.frame * self.hit_size[0], 0, self.hit_size[0], self.hit_size[1], 0, 'h',
                                     self.m_x, self.m_y + 20, self.hit_size[0] // 3, self.hit_size[1] // 3)

    def frame_state(self):
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

    # def change_state(self, num):
    #     if num == 0:
    #         self.state = 0
    #     elif num == 1:
    #         self.state = 1
    #     elif num == 2:
    #         self.state = 2
    #     elif num == 3:
    #         self.state = 3

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
            self.dir_y = 0
            if self.look_at == -1:
                self.m_x += 35  # flip x좌표 이미지 보정
        elif self.m_y < 90:
            if self.dir_x == 0:
                self.state = 0
            else:
                self.state = 1
            self.m_y = 90
            self.dir_y = 0
            if self.look_at == -1:
                self.m_x += 35  # flip x좌표 이미지 보정

    def catch_event(self):
        if self.state == 3:
            return
        events = get_events()
        for event in events:
            if event.type == SDL_KEYDOWN:
                if event.key == SDLK_UP:
                    if (self.box[0] > 300 - 70 and self.box[2] < 300 + 70) and self.m_y == 90:
                        self.state = 2
                        self.m_x = 280
                        self.m_y += 5
                        self.dir_y += 1
                    elif (self.box[0] > 800 - 70 and self.box[2] < 800 + 70) and self.m_y == 90:
                        self.state = 2
                        self.m_x = 780
                        self.m_y += 5
                        self.dir_y += 1
                    elif self.state == 2:
                        self.dir_y += 1
                elif event.key == SDLK_DOWN:
                    if (self.box[0] > 300 - 70 and self.box[2] < 300 + 70) and self.m_y == 300:
                        self.state = 2
                        self.m_x = 280
                        self.m_y -= 5
                        self.dir_y -= 1
                    elif (self.box[0] > 800 - 70 and self.box[2] < 800 + 70) and self.m_y == 300:
                        self.state = 2
                        self.m_x = 780
                        self.m_y -= 5
                        self.dir_y -= 1
                    elif self.state == 2:
                        self.dir_y -= 1
                elif event.key == SDLK_RIGHT:
                    if self.state != 2:
                        self.state = 1
                    self.dir_x += 1
                    if self.dir_x == 0 and self.state != 2:
                        self.state = 0
                elif event.key == SDLK_LEFT:
                    if self.state != 2:
                        self.state = 1
                    self.dir_x -= 1
                    if self.dir_x == 0 and self.state != 2:
                        self.state = 0
                elif event.key == SDLK_SPACE and self.state != 2:
                    self.frame = 0
                    self.state = 3
            elif event.type == SDL_KEYUP:
                if event.key == SDLK_UP:
                    if self.state == 2:
                        self.dir_y -= 1
                elif event.key == SDLK_DOWN:
                    if self.state == 2:
                        self.dir_y += 1
                elif event.key == SDLK_RIGHT:
                    self.dir_x -= 1
                    if self.dir_x == 0 and self.state != 2:
                        self.state = 0
                    elif self.state != 2:
                        self.state = 1
                elif event.key == SDLK_LEFT:
                    self.dir_x += 1
                    if self.dir_x == 0 and self.state != 2:
                        self.state = 0
                    elif self.state != 2:
                        self.state = 1
        if self.dir_x > 0:
            self.look_at = 1
        elif self.dir_x < 0:
            self.look_at = -1


class NonePlayableCharacter(Character):
    def __init__(self, i_x=0, i_y=0, i_attack=0, i_health = 0):
        super().__init__(i_x, i_y, i_attack)
        self.health_point = i_health
        self.dir_x = 1
        self.state = 1
        self.cool_time = 0
    pass


class WarriorCharacter(NonePlayableCharacter):
    def __init__(self):
        super().__init__(90, 110, 5, 50)
        self.idle_size = (121, 106)
        self.run_size = (131, 158)
        self.hit_size = (198, 175)
        self.frame_mouse = 0 # 기존 프레임 레이트에 맞추기 위한 마우스 프레임

    def idle(self): # +35, -20 스프라이트 오차 수정
        warrior_idle.clip_composite_draw(self.idle_size[0] * self.frame, 0, self.idle_size[0], self.idle_size[1], 0, 'h',
                                        self.m_x + 35, self.m_y - 20, self.idle_size[0], self.idle_size[1])

    def hit(self): # +17, +15 스프라이트 오차 수정
        warrior_hit.clip_composite_draw(self.hit_size[0] * self.frame, 0, self.hit_size[0], self.hit_size[1], 0, 'h',
                                        self.m_x + 17, self.m_y + 15, self.hit_size[0], self.hit_size[1])

    def run(self):
        warrior_run.clip_composite_draw(self.run_size[0] * self.frame, 0, self.run_size[0], self.run_size[1], 0, 'h',
                                       self.m_x, self.m_y, self.run_size[0], self.run_size[1])

    def frame_state(self):
        if self.state == 0:
            self.idle()
        elif self.state == 1:
            self.run()
        elif self.state == 2:
            self.hit()

    def frame_rate(self):
        if self.state == 0:  # idle
            self.frame = (self.frame + 1) % 8
            # 적이 없으면 상태 바꿔야함
            # if self.check_enemy == False:
            # elif self.cool_time == 0:
            #   self.state = 2
            #   self.frame = 0
            if self.cool_time == 0: # 임시로 해둔 것
                self.state = 2
                self.frame = 0
        elif self.state == 1:  # run
            self.frame = (self.frame + 1) % 16
        elif self.state == 2:  # hit
            self.frame = (self.frame + 1) % 16
            if self.frame == 0:
                self.state = 0
                self.cool_time = 100

    def hit_cool_time(self):
        if self.cool_time != 0:
            self.cool_time -= 1

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

class EnemyCharacter(Character):
    dir_x = -1
    health_point = 70
    def __init__(self):
        self.m_x = 1200
        self.m_y = 80
        self.attack_damage = 10


class Castle:
    def __init__(self):
        self.m_x = 0
        self.m_y = 245
        self.health_point = 1000
        self.Castle_img = load_image("image/castle.png")

    def draw_castle(self):
        self.Castle_img.draw(self.m_x, self.m_y)


def draw_back_ground():
    ladder_pos_x = (300, 800)
    ladder_pos_y = 160
    backGround.draw(width // 2, height // 2)
    castle.draw_castle()
    for x in range(98, width, tile_width):
        floor.draw(x, 245)
        x = x + tile_width
    ladder.draw(ladder_pos_x[0], ladder_pos_y)
    ladder.draw(ladder_pos_x[1], ladder_pos_y)


hero = MainCharacter()
warrior = WarriorCharacter()
castle = Castle()


def user_event(i_hero):
    i_hero.catch_event()
    i_hero.frame_state()
    i_hero.frame_rate()
    i_hero.move()


def friendly_event(i_warrior):
    i_warrior.hit_cool_time()
    i_warrior.frame_state()
    i_warrior.frame_rate()
    i_warrior.move()


def reset_world():
    pass


def update_world():
    draw_back_ground()
    friendly_event(warrior)
    user_event(hero)
    pass

# class UserClass:
#     def __init__(self):
#         self.player = MainCharacter()
#         self.gameRun = True
#
#     def catch_events(self):
#         events = get_events()
#         for event in events:
#             if event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
#                 self.gameRun = False
#
# user = UserClass()

while True:
    clear_canvas()
    update_world()
    update_canvas()
    delay(0.03)


