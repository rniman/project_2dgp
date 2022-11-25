import game_framework
import title_state
import play_state
from pico2d import *
from exit_button import Exit
from replay_button import Replay

back_board = None
replay_bt = None
exit_bt = None
over_font = None

def enter():
    global back_board, replay_bt, exit_bt, over_font
    back_board = load_image('image/window_background.png')
    over_font = load_font('font/megadeth.ttf', 70)
    replay_bt = Replay()
    exit_bt = Exit()


def exit():
    global back_board, replay_bt, exit_bt, over_font
    del back_board
    del replay_bt
    del exit_bt
    del over_font

def update():
    handle_events()

def draw():
    back_board.clip_draw(0, 0, 500, 500, 1280 / 2, 720 / 2, 420, 420)
    replay_bt.draw()
    exit_bt.draw()
    over_font.draw(1280 / 2 - 170, 720 / 2 + 140, f'GAME OVER', (245, 10, 10))
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
            elif event.y >=  720 / 2 + 100 - 142 / 4 and event.y <= 720 / 2 + 100 + 142 / 4:
                game_framework.pop_state()
                game_framework.change_state(title_state)

def pause():
    pass

def resume():
    pass

