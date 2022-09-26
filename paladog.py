from pico2d import *

width = 1280
height = 720

open_canvas(width, height)

backGround = load_image('image/Bground.png')
Grass = load_image('image/Grass.png')
Mouse = load_image('image/mouse1.png')
backGround.draw(width // 2, height// 2)

Mouse.draw(500,90)

Grass.draw(width // 2, height//2)

update_canvas()
input()

