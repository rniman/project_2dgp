from pico2d import *
import random
import game_framework
import game_world
import server
import json

import pause_state
from castle import Castle
from back_ground import BackGround
from floor import Floor
from ladder import Ladder
from main_character import MainCharacter
from decor import Decor
from pause_button import Pause
from clear_time import Clear_time

import enemy_warrior

selected_difficulty = None
back_ground = None
ladder = None
floor = None
decor = None
castle = None
pause_bt = None
play_time = None
clear_time = None
time_font = None
music = None

# 초기화
def enter():
    global selected_difficulty
    global pause_bt
    global back_ground, ladder, floor, decor
    global castle
    global play_time, clear_time
    global music

    with open('select_difficulty.json', 'r') as file:
        selected_difficulty = json.load(file)

    play_time = 0
    clear_time = Clear_time(120)

    pause_bt = Pause()

    back_ground = BackGround()
    ladder = [Ladder(300), Ladder(800)]
    floor = Floor()
    castle = Castle()
    decor = [Decor(270), Decor(200)]

    game_world.add_object(back_ground, 0)
    game_world.add_object(floor, 0)
    game_world.add_objects(ladder, 0)
    game_world.add_object(pause_bt, 0)
    game_world.add_object(clear_time, 0)
    game_world.add_object(castle, 1)
    game_world.add_object(decor[0], 0)
    game_world.add_object(decor[1], 5)

    game_world.add_collision_pairs(castle, None, 'castle:eWar')

    server.main_character = MainCharacter()
    game_world.add_object(server.main_character, 4)
    music = load_music('music/play_bgm.mp3')
    music.play()


# 종료
def exit():
    global pause_bt
    global back_ground, ladder, floor, decor
    global castle
    global play_time, clear_time
    global music

    del pause_bt, back_ground, ladder, floor, decor, castle, play_time, clear_time
    del server.main_character
    game_world.clear()
    music.stop()
    del music


# 월드의 존재하는 객체들을 업데이트
# 임시로 5초마다 적 생성
def update():
    global selected_difficulty, play_time, clear_time
    play_time += game_framework.frame_time
    summon_number = 1

    for game_object in game_world.all_objects():
        if game_object != None:
            game_object.update()

    if play_time >= 2.0:
        if selected_difficulty == 'easy':
            if clear_time.get_time() < 50.0:
                summon_number = random.randint(1, 2)
            if clear_time.get_time() < 25.0:
                summon_number = 2
        elif selected_difficulty == 'hard':
            if clear_time.get_time() < 60.0:
                summon_number = 2
            if clear_time.get_time() < 30.0:
                summon_number = random.randint(2, 3)

        for i in range(summon_number):
            ewarrior = enemy_warrior.EnemyWarrior(random.randint(1, 2))
            game_world.add_object(ewarrior, 2)
            game_world.add_collision_pairs(None, ewarrior, 'war:eWar')
            game_world.add_collision_pairs(None, ewarrior, 'castle:eWar')
        play_time = 0.0

    for fir, sec, group in game_world.all_collision_pairs():
        if collide(fir, sec):
            fir.collide(sec, group)
            sec.collide(fir, group)

def draw_world():
    for game_object in game_world.all_objects():
        if game_object != None:
            game_object.draw()

# 월드를 그린다
def draw():
    clear_canvas()
    draw_world()
    update_canvas()

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_MOUSEBUTTONDOWN:
            if event.y <= 720 - (660 + 25):
                continue
            if event.y >= 720 - (660 - 25):
                continue
            if event.x <= 1220 - 19:
                continue
            if event.x >= 1220 + 19:
                continue
            game_framework.push_state(pause_state)
        else:
            server.main_character.handle_event(event)


def collide(first, second):  # 두개의 객체가 사각형이라는 전제
    left_fir, bottom_fir, right_fir, top_fir = first.get_bounding_box()
    left_sec, bottom_sec, right_sec, top_sec = second.get_bounding_box()

    if left_fir > right_sec: return False
    if right_fir < left_sec: return False
    if top_fir < bottom_sec: return False
    if bottom_fir > top_sec: return False

    return True

def pause():
    pass

def resume():
    pass