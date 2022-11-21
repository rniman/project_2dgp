from pico2d import *
import game_framework

import play_state
import guide_state
from start_button import Start
from tutorial_button import Tutorial
from exit_button import Exit

image = None
font = None
window = None
button = None
start_bt = None
tutorial_bt = None
exit_bt = None

def enter():
    global image, font, window, button
    global start_bt, exit_bt, tutorial_bt
    image = load_image('image/title_background.png')
    font = load_font('font/Arial_Black.ttf', 25)
    window = load_image('image/Window_Background.png')
    start_bt = Start()
    tutorial_bt = Tutorial()
    exit_bt = Exit()

def exit():
    global image
    del image

def update():
    handle_events()
    pass

def draw():
    clear_canvas()
    image.clip_draw(0, 0, 1280, 720, 1280 / 2, 720 / 2, 1280, 720)
    window.clip_draw(0, 0, 500, 500, 1280 / 2, 720 / 2)
    start_bt.draw()
    tutorial_bt.draw()
    exit_bt.draw()
    update_canvas()

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_MOUSEBUTTONDOWN:
            if event.x <= 1280 / 2 - 454 / 3:
                continue
            if event.x >= 1280 / 2 + 454 / 3:
                continue
            if event.y <= 720 / 2 - 100 - 142 / 4:
                continue
            if event.y >= 720 / 2 + 100 + 142 / 4:
                continue

            if event.y >= 720 / 2 - 142 / 4 and event.y <= 720 / 2 + 142 / 4:
                game_framework.push_state(guide_state)
            elif event.y >= 720 / 2 - 100 - 142 / 4 and event.y <= 720 / 2 - 100 + 142 / 4:
                game_framework.change_state(play_state)
            elif event.y >=  720 / 2 + 100 - 142 / 4 and event.y <= 720 / 2 + 100 + 142 / 4:
                game_framework.quit()

def pause():
    pass

def resume():
    pass

