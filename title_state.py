from pico2d import *
import game_framework
import guide_state
import select_difficulty_state
from play_button import Play
from tutorial_button import Tutorial
from exit_button import Exit
from title_back_ground import BackGround

background = None
play_bt = None
tutorial_bt = None
exit_bt = None

def enter():
    global background
    global play_bt, exit_bt, tutorial_bt
    background = BackGround()

    play_bt = Play()
    tutorial_bt = Tutorial()
    exit_bt = Exit()

def exit():
    global background
    global play_bt, exit_bt, tutorial_bt
    del background, play_bt, exit_bt, tutorial_bt

def update():
    handle_events()
    pass

def draw():
    clear_canvas()
    background.draw()
    play_bt.draw()
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
                game_framework.push_state(select_difficulty_state)
            elif event.y >=  720 / 2 + 100 - 142 / 4 and event.y <= 720 / 2 + 100 + 142 / 4:
                game_framework.quit()

def pause():
    pass

def resume():
    pass

