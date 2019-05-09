import pygame as pg
import os
import renderer as rend

pg.init()
screen = pg.display.set_mode((1000, 750))
done = False
clock = pg.time.Clock()
 
while not done:
        for event in pg.event.get():
                if event.type == pg.QUIT:
                        done = True
         
        screen.fill((255, 255, 255))
         
        pg.display.flip()
        clock.tick(60)