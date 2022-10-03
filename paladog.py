from pico2d import *

width = 1280
height = 720

tile_width = 90

open_canvas(width, height)

backGround = load_image('image/Bground.png')
Grass = load_image('image/Grass.png')
Mouse = load_image('image/mouse_move.png')
floor = load_image('image/tile.png')
ladder = load_image('image/ladder2.png')

main_idle = load_image('image/main_idle.png')
main_run = load_image('image/main_run.png')
main_hit = load_image('image/main_hit.png')
main_cilmb = load_image('image/main_climb.png')

class Character:
    state = 0
    frame = 0
    m_x = 0
    m_y = 0
    attack_damage = 0


#1층에서 120
class main_Character(Character):
    idle_size = (373, 286)
    run_size = (428, 331)
    climb_size = (376, 262)
    hit_size = (647, 504)
    box = []
    dir_x = 0
    dir_y = 0
    look_at = 1
    def __init__(self):
        self.m_x = 100
        self.m_y = 90
        self.box = [self.m_x, self.m_y, self.m_x + self.idle_size[0]//6, self.m_y + self.idle_size[1]//3]

    def frame_rate(self):
        if self.state == 0:
            self.frame = (self.frame + 1) % 8
        elif self.state == 1:
            self.frame = (self.frame + 1) % 8
        elif self.state == 2:
            self.frame = (self.frame + 1) % 8
        elif self.state == 3:
            self.frame = (self.frame + 1) % 12
            if(self.frame == 0):
                if self.dir_x == 0:
                    self.state = 0
                else:
                    self.state = 1
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
        main_cilmb.clip_draw(0 + self.frame * self.climb_size[0], 0, self.climb_size[0], self.climb_size[1], self.m_x, self.m_y,
                           self.climb_size[0] // 3, self.climb_size[1] // 3)
    def hit(self):  # y, 120
        main_hit.clip_draw(0 + self.frame * self.hit_size[0], 0, self.hit_size[0], self.hit_size[1], self.m_x, self.m_y + 20,
                           self.hit_size[0] // 3, self.hit_size[1] // 3)
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
    def change_state(self, num):
        if num == 0:
            self.state = 0
        elif num == 1:
            self.state = 1
        elif num == 2:
            self.state = 2
        elif num == 3:
            self.state = 3
    def move(self):
        if self.state == 1 or self.state == 0:
            self.m_x += self.dir_x * 5
            if self.m_x > 1200:
                self.m_x = 1200
            elif self.m_x < 100:
                self.m_x = 100

            if self.look_at == 1:
                self.box = [self.m_x, self.m_y, self.m_x + self.idle_size[0] // 6, self.m_y + self.idle_size[1] // 3]
            else:
                self.box = [self.m_x - self.idle_size[0] // 6, self.m_y, self.m_x, self.m_y - self.idle_size[1] // 3]
        elif self.state == 2:
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

class friendly_Character(Character):
    def __init__(self):
        self.move_size = (87, 80)
        self.m_x = 90
        self.m_y = 80
        self.attack_damage = 5
        self.health_point = 50
        self.dir_x = 1
        self.frame_mouse = 0
    def frame_rate(self):
        self.frame_mouse += 1
        if self.frame_mouse % 8 == 0:
            self.frame = (self.frame + 1) % 3

    def run(self):
        Mouse.clip_draw(87 * self.frame, 0, self.move_size[0], self.move_size[1], self.m_x, self.m_y)

    def move(self):
        self.m_x += self.dir_x * 1
        if self.m_x > 1240:
            self.m_x = 1240

class enemy_Character(Character):
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
        self.Castle_img = load_image("image/castle02.png")

    def draw_castle(self):
        self.Castle_img.draw(self.m_x, self.m_y)

def draw_backGround():
    ladder_posx = (300, 800)
    ladder_posy = 160
    backGround.draw(width // 2, height // 2)
    castle.draw_castle()
    for x in range(98, width, tile_width):
        floor.draw(x, 245)
        x = x + tile_width
    ladder.draw(ladder_posx[0], ladder_posy)
    ladder.draw(ladder_posx[1], ladder_posy)

user = main_Character()
mouse01 = friendly_Character()
castle = Castle()

while True:
    clear_canvas()
    draw_backGround()
    user.catch_event()
    user.frame_state()
    user.frame_rate()
    user.move()

    mouse01.run()
    mouse01.frame_rate()
    mouse01.move()
    update_canvas()
    delay(1/60)




input()

