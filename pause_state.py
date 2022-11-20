from pico2d import *
import game_framework
import play_state

# fill here
# running = True -> game_framework에서 다룸
image = None
logo_Time = 0.0

def enter():
    global image
    image = load_image('image/tuk_credit.png')

def exit():
    global image
    del image

def update():
    global logo_Time  # ,  running
    # logo_Time += game_framework.frame_time
    if logo_Time >= 3.0:
        logo_Time = 0.0
        game_framework.change_state(play_state)

def draw():
    clear_canvas()
    image.draw(1280 // 2, 720 // 2)
    update_canvas()


def handle_events():
    pass



