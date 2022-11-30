
import game_framework
import play_state
import json

from pico2d import *
from easy_button import Easy
from hard_button import Hard
from exit_button import Exit

back_board = None
easy_bt = None
hard_bt = None
exit_bt = None

def enter():
    global back_board, easy_bt, hard_bt, exit_bt
    back_board = load_image('image/window_background.png')
    easy_bt = Easy()
    hard_bt = Hard()
    exit_bt = Exit()

def exit():
    global back_board, easy_bt, hard_bt, exit_bt
    del back_board
    del easy_bt
    del hard_bt
    del exit_bt

def update():
    handle_events()

def draw():
    back_board.clip_draw(0, 0, 500, 500, 640, 360, 400, 400)
    hard_bt.draw()
    easy_bt.draw()
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
                select_difficulty = "hard"
                with open('select_difficulty.json', 'w') as file:
                    json.dump(select_difficulty, file)
                game_framework.pop_state()
                game_framework.pop_state()
                game_framework.change_state(play_state)

            elif event.y >= 720 / 2 - 100 - 142 / 4 and event.y <= 720 / 2 - 100 + 142 / 4:
                select_difficulty = "easy"
                with open('select_difficulty.json', 'w') as file:
                    json.dump(select_difficulty, file)
                game_framework.pop_state()
                game_framework.pop_state()
                game_framework.change_state(play_state)

            elif event.y >= 720 / 2 + 100 - 142 / 4 and event.y <= 720 / 2 + 100 + 142 / 4:
                game_framework.pop_state()

def pause():
    pass

def resume():
    pass

