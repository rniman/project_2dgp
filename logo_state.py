from pico2d import *
import game_framework

import title_state
import play_hard_state

image = None
logo_Time = 0.0

def enter():
    global image
    image = load_image('image/tuk_credit.png')

def exit():
    global image
    del image

def update():
    # logo time을 계산하고 1초가 넘으면 running을 false로
    global logo_Time, running
    logo_Time += game_framework.frame_time
    if logo_Time >= 3.0: # 로고타임off
        logo_Time = 0.0
        running = False
        game_framework.change_state(title_state)

def draw():
    clear_canvas()
    image.draw(1280 // 2, 720 // 2)
    update_canvas()

def handle_events():
    pass
    # events = get_events()
    # for event in events:
    #     if event.type == SDL_KEYDOWN and event.key == SDLK_z:
    #         game_framework.change_state(play_state)



