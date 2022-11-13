from pico2d import *
import game_framework

import play_state

image = None
logo_Time = 0.0

def enter():
    global image, dir_x, dir_y
    image = load_image('image/tuk_credit.png')
    dir_x = 0
    dir_y = 0

def exit():
    global image
    del image

def update():
    # logo time을 계산하고 1초가 넘으면 running을 false로
    global logo_Time, running
    delay(0.01)
    logo_Time += 0.01
    if logo_Time >= 1.0: # 로고타임off
        logo_Time = 0.0
        running = False
        game_framework.change_state(play_state)

def draw():
    clear_canvas()
    image.draw(1280 // 2, 720 // 2)
    update_canvas()


def handle_events():
    pass



