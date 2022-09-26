from pico2d import *

width = 1280
height = 720

tile_width = 90

open_canvas(width, height)

backGround = load_image('image/Bground.png')
Grass = load_image('image/Grass.png')
Mouse = load_image('image/mouse1.png')
Castle = load_image("image/castle02.png")
floor =  load_image('image/tile.png')
ladder = load_image('image/ladder2.png')
backGround.draw(width // 2, height// 2)

x = 98



Castle.draw(0,250)
Mouse.draw(90,80)


while(x < width):
    floor.draw(x,250)
    x = x + tile_width
ladder.draw(300,160)
ladder.draw(800,160)


Grass.draw(width // 2, height//2 - 50)

update_canvas()
input()

