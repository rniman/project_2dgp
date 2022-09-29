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
    hit_size = (647, 504)

    def __init__(self):
        self.m_x = 100
        self.m_y = 90
    def frame_rate(self):
        if self.state == 0:
            self.frame = (self.frame + 1) % 8
        elif self.state == 3:
            self.frame = (self.frame + 1) % 12

    def main_idle(self):
        main_idle.clip_draw(0 + self.frame * self.idle_size[0], 0, self.idle_size[0], self.idle_size[1], self.m_x, self.m_y, self.idle_size[0] // 3, self.idle_size[1] // 3)
    def main_hit(self):# y, 120
        main_hit.clip_draw(0 + self.frame * self.hit_size[0], 0, self.hit_size[0], self.hit_size[1], self.m_x, self.m_y, self.hit_size[0] // 3, self.hit_size[1] // 3)


def draw_backGround():
    backGround.draw(width // 2, height // 2)
    Castle.draw(0,250)
    for x in range(98, width, tile_width):
        floor.draw(x, 250)
        x = x + tile_width
    ladder.draw(300, 160)
    ladder.draw(800, 160)


a = main_Character()

while True:
    clear_canvas()
    draw_backGround()
    Mouse.draw(90, 80)
    a.main_idle()
    a.frame_rate()

    update_canvas()
    delay(0.01)

#Grass.draw(width // 2, height//2 - 50)

input()

