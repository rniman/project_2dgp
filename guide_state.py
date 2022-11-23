from pico2d import *
import game_framework

image = None
font = None
back_board = None
button = None

def enter():
    global image, font, back_board, button
    image = load_image('image/title_background.png')
    font = load_font('font/kozuka_gothic_bold.otf', 40)
    back_board = load_image('image/window_background.png')
    button = load_image('image/decline.png')

def exit():
    global image, font, back_board, button
    del image
    del font
    del back_board
    del button

def update():
    handle_events()

def draw():
    clear_canvas()
    image.clip_draw(0, 0, 1280, 720, 1280 / 2, 720 / 2, 1280, 720)
    back_board.clip_draw(0, 0, 500, 500, 1280 / 2, 720 / 2, 1000, 700)
    button.clip_draw(0, 0, 68, 71, 1050, 630)
    font.draw(230, 320, f'SPACE: ATTACK', (200, 200, 200))
    font.draw(230, 420, f'Arrow Key: MOVE', (200, 200, 200))
    font.draw(230, 220, f'KEY ''1'': SUMMON WARRIOR FIRST FLOOR', (200, 200, 200))
    font.draw(230, 120, f'KEY ''5'': SUMMON WARRIOR SECOND FLOOR', (200, 200, 200))
    font.draw(230, 620, f'GOAL: Defend the castle', (200, 200, 200))
    font.draw(230, 520, f'DEFEAT: A castle collapses', (200, 200, 200))
    update_canvas()

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_MOUSEBUTTONDOWN:
            if event.x <= 1050 - 34:
                continue
            if event.x >= 1050 + 34:
                continue
            if event.y <= 720 - (630 + 71 / 2):
                continue
            if event.y >= 720 - (630 - 71 / 2):
                continue
            game_framework.pop_state()





