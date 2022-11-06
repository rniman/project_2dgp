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

from castle import Castle
from back_ground import BackGround
from floor import Floor
from ladder import Ladder
from main_character import MainCharacter
from warrior import Warrior
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
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
            elif event.key == SDLK_q:
                for war in warrior:
                    war.state = -1
            elif event.key == SDLK_w:
                for ewar in e_warrior:
                    ewar.state = -1
            elif event.key == SDLK_UP:
                mainChar.dir_y += 1
                if (mainChar.box[0] > 300 - 70 and mainChar.box[2] < 300 + 70):
                    if mainChar.m_y == 90:
                        mainChar.state = 2
                        mainChar.m_x = 280
                        mainChar.m_y += 5
                elif (mainChar.box[0] > 800 - 70 and mainChar.box[2] < 800 + 70):
                    if mainChar.m_y == 90:
                        mainChar.state = 2
                        mainChar.m_x = 780
                        mainChar.m_y += 5
            elif event.key == SDLK_DOWN:
                mainChar.dir_y -= 1
                if (mainChar.box[0] > 300 - 70 and mainChar.box[2] < 300 + 70):
                    if mainChar.m_y == 300:
                        mainChar.state = 2
                        mainChar.m_x = 280
                        mainChar.m_y -= 5
                elif (mainChar.box[0] > 800 - 70 and mainChar.box[2] < 800 + 70):
                    if mainChar.m_y == 300:
                        mainChar.state = 2
                        mainChar.m_x = 780
                        mainChar.m_y -= 5
            elif event.key == SDLK_RIGHT:
                if mainChar.state != 2:
                    mainChar.state = 1
                mainChar.dir_x += 1
                if mainChar.dir_x == 0 and mainChar.state != 2:
                    mainChar.state = 0
            elif event.key == SDLK_LEFT:
                if mainChar.state != 2:
                    mainChar.state = 1
                mainChar.dir_x -= 1
                if mainChar.dir_x == 0 and mainChar.state != 2:
                    mainChar.state = 0
            elif event.key == SDLK_SPACE and mainChar.state != 2:
                mainChar.frame = 0
                mainChar.state = 3
            elif event.key == SDLK_1 and mainChar.now_resource >= 100:
                mainChar.now_resource -= 100
                warrior.append(Warrior(1))
            elif event.key == SDLK_5 and mainChar.now_resource >= 100:
                mainChar.now_resource -= 100
                warrior.append(Warrior(5))

        elif event.type == SDL_KEYUP:
            if event.key == SDLK_UP:
                mainChar.dir_y -= 1
            elif event.key == SDLK_DOWN:
                mainChar.dir_y += 1
            elif event.key == SDLK_RIGHT:
                mainChar.dir_x -= 1
                if mainChar.dir_x == 0 and mainChar.state != 2:
                    mainChar.state = 0
                elif mainChar.state != 2:
                    mainChar.state = 1
            elif event.key == SDLK_LEFT:
                mainChar.dir_x += 1
                if mainChar.dir_x == 0 and mainChar.state != 2:
                    mainChar.state = 0
                elif mainChar.state != 2:
                    mainChar.state = 1

        if mainChar.dir_x > 0:
            mainChar.look_at = 1
        elif mainChar.dir_x < 0:
            mainChar.look_at = -1

# 초기화
def enter():
    global back_ground, ladder, floor
    global castle
    global mainChar
    global warrior
    global e_warrior
    back_ground = BackGround()
    ladder = Ladder()
    floor = Floor()
    castle = Castle()
    mainChar = MainCharacter()
    warrior = []
    e_warrior = []

# 종료
def exit():
    del back_ground
    del ladder
    del floor
    del castle
    del mainChar
    del warrior
    del e_warrior

# 월드의 존재하는 객체들을 업데이트
def update():
    global time
    for w in warrior:
        if w.update() == -1:
            warrior.remove(w)
    for ew in e_warrior:
        if ew.update() == -1:
            e_warrior.remove(ew)

    mainChar.update()

    if time % 100 == 0:
        e_warrior.append(EnemyWarrior())
    time += 1
    delay(0.03)

# 월드를 그린다
def draw():
    clear_canvas()
    back_ground.draw()
    castle.draw()
    floor.draw()
    ladder.draw()

    mainChar.draw()

    for w in warrior:
        w.draw()
    for ew in e_warrior:
        ew.draw()

    update_canvas()




