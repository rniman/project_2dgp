from pico2d import *

width = 1280
height = 720

tile_width = 90

open_canvas(width, height)

backGround = load_image('image/Bground.png')
Grass = load_image('image/Grass.png')
Mouse = load_image('image/mouse1.png')
Castle = load_image("image/castle02.png")
floor = load_image('image/tile.png')
ladder = load_image('image/ladder2.png')



class Character:
    state = 0
    frame = 0
    m_x = 0
    m_y = 0

main_idle = load_image('image/main_idle.png')
main_run = load_image('image/main_run.png')
main_hit = load_image('image/main_hit.png')
main_cilmb = load_image('image/main_climb.png')
#1층에서 120
class main_Character(Character):
    idle_size = (373, 286)
    run_size = (428, 331)
    climb_size = (376, 262)
    hit_size = (647, 504)
    box = []
    dir = 0
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
                if self.dir == 0:
                    self.state = 0
                else:
                    self.state = 1

    def main_idle(self):
        main_idle.clip_draw(0 + self.frame * self.idle_size[0], 0, self.idle_size[0], self.idle_size[1], self.m_x, self.m_y,
                            self.idle_size[0] // 3, self.idle_size[1] // 3)
    def main_run(self):
        main_run.clip_draw(0 + self.frame * self.run_size[0], 0, self.run_size[0], self.run_size[1], self.m_x, self.m_y,
                           self.run_size[0] // 3, self.run_size[1] // 3)
    def main_climb(self):
        main_cilmb.clip_draw(0 + self.frame * self.climb_size[0], 0, self.climb_size[0], self.climb_size[1], self.m_x, self.m_y,
                           self.climb_size[0] // 3, self.climb_size[1] // 3)
    def main_hit(self):  # y, 120
        main_hit.clip_draw(0 + self.frame * self.hit_size[0], 0, self.hit_size[0], self.hit_size[1], self.m_x, self.m_y + 20,
                           self.hit_size[0] // 3, self.hit_size[1] // 3)

    def frame_state(self):
        if self.state == 0:
            self.main_idle()
        elif self.state == 1:
            self.main_run()
        elif self.state == 2:
            self.main_climb()
        elif self.state == 3:
            self.main_hit()
    def move_charcter(self):
        if self.state == 1 or self.state == 0:
            self.m_x += self.dir * 5
            self.box = [self.m_x, self.m_y, self.m_x + self.idle_size[0] // 6, self.m_y + self.idle_size[1] // 3]
    def catch_event(self):
        if self.state == 3:
            return
        events = get_events()
        for event in events:
            if event.type == SDL_KEYDOWN:
                if event.key == SDLK_RIGHT:
                    self.state = 1
                    self.dir += 1
                    if self.dir == 0:
                        self.state = 0
                elif event.key == SDLK_LEFT:
                    self.state = 1
                    self.dir -= 1
                    if self.dir == 0:
                        self.state = 0
                elif event.key == SDLK_UP:
                    if self.box[0] > 300 - 50 and self.box[2] < 300 + 70:
                        self.state = 2
                elif event.key == SDLK_SPACE:
                    self.frame = 0
                    self.state = 3
            elif event.type == SDL_KEYUP:
                if event.key == SDLK_RIGHT:
                    self.dir -= 1
                    if self.dir == 0:
                        self.state = 0
                    else:
                        self.state = 1
                elif event.key == SDLK_LEFT:
                    self.dir += 1
                    if self.dir == 0:
                        self.state = 0
                    else:
                        self.state = 1

def draw_backGround():
    global ladder_posx,ladder_posy
    ladder_posx = (300, 800)
    ladder_posy = 160
    backGround.draw(width // 2, height // 2)
    Castle.draw(0,250)
    for x in range(98, width, tile_width):
        floor.draw(x, 250)
        x = x + tile_width
    ladder.draw(ladder_posx[0], ladder_posy)
    ladder.draw(ladder_posx[1], ladder_posy)




a = main_Character()

while True:
    clear_canvas()
    draw_backGround()
    Mouse.draw(90, 80)
    a.catch_event()
    a.frame_state()
    a.frame_rate()
    a.move_charcter()
    update_canvas()
    delay(0.05)

#Grass.draw(width // 2, height//2 - 50)

input()

