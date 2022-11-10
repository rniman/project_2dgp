back_ground = None
ladder = None
floor = None
castle = None
mainChar = None
warrior = None
e_warrior = None
time = 0

from pico2d import *
import game_framework
import logo_state
import game_world

from castle import Castle
from back_ground import BackGround
from floor import Floor
from ladder import Ladder
from main_character import MainCharacter
from enemy_warrior import EnemyWarrior

width = 1280
height = 720
bar_width = 1808
bar_height = 124
col_bar_width = 1730
col_bar_height = 66

def handle_events():
    global mainChar
    global warrior
    events = get_events()
    for event in events:
        if event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_q:
            for war in game_world.game_object[2]:
                war.state = -1
        elif event.type == SDL_KEYDOWN and event.key == SDLK_w:
            for ewar in game_world.game_object[1]:
                ewar.state = -1
        else:
            mainChar.handle_event(event)

# 초기화
def enter():
    global back_ground, ladder, floor
    global castle
    global warrior, e_warrior
    global mainChar
    back_ground = BackGround()
    ladder = Ladder()
    floor = Floor()
    castle = Castle()

    game_world.add_object(back_ground, 0)
    game_world.add_object(ladder, 0)
    game_world.add_object(floor, 0)
    game_world.add_object(castle, 0)

    mainChar = MainCharacter()
    game_world.add_object(mainChar, 3)

# 종료
def exit():
    game_world.clear()

# 월드의 존재하는 객체들을 업데이트
def update():
    for game_object in game_world.all_objects():
        if game_object != None:
            game_object.update()
    global time
    time += 1
    if time % 100 == 0:
        enemy_warrior = EnemyWarrior()
        game_world.add_object(enemy_warrior, 1)
    delay(0.03)

def draw_world():
    for game_object in game_world.all_objects():
        if game_object != None:
            game_object.draw()

# 월드를 그린다
def draw():
    clear_canvas()
    draw_world()
    update_canvas()





