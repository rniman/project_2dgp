import game_framework
import title_state
import play_state
from pico2d import *
from play_button import Play
from exit_button import Exit
from replay_button import Replay

back_board = None
replay_bt = None
exit_bt = None

def enter():
    global back_board, replay_bt, exit_bt
    back_board = load_image('image/window_background.png')
    replay_bt = Replay()
    exit_bt = Exit()

def exit():
    global back_board, replay_bt, exit_bt
    del back_board
    del replay_bt
    del exit_bt

def update():
    handle_events()

def draw():
    back_board.clip_draw(0, 0, 500, 500, 1280 / 2, 720 / 2)
    replay_bt.draw()
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
                game_framework.pop_state()
                game_framework.change_state(play_state)
            elif event.y >= 720 / 2 - 100 - 142 / 4 and event.y <= 720 / 2 - 100 + 142 / 4:
                game_framework.pop_state()
            elif event.y >=  720 / 2 + 100 - 142 / 4 and event.y <= 720 / 2 + 100 + 142 / 4:
                game_framework.pop_state()
                game_framework.change_state(title_state)

def pause():
    pass

def resume():
    pass

