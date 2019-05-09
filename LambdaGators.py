import pygame as pg
import os
import random

def randomColor():
        x = random.randint(10, 240)
        y = random.randint(10, 240)
        z = random.randint(10, 240)

        return (x, y, z, 0)

def render(varList):
        baseColor = (0, 0, 0) #constant value of the base color gator 
        thresh = (0, 0, 0) #threshold value for pygame transform 

        imgDict = {} #dictionary of variables to reference alligator/func or egg/var of variable specific color

        for var in varList:
                imgDict[var] = {} #sub-dictionary per variable
                
                newColor = randomColor() #new random color for new var
                
                tempGator = pg.image.load('Resources/alligator.png') #loads temp Surfaces
                tempEgg = pg.image.load('Resources/egg.png')

                pg.transform.threshold(tempGator, tempGator, baseColor, thresh, newColor, 1, None, False) #makes Surfaces the new var color
                pg.transform.threshold(tempEgg, tempEgg, baseColor, thresh, newColor, 1, None, False) 

                imgDict[var]['alligator'] = tempGator #adds gator and egg to var sub-dict 
                imgDict[var]['egg'] = tempEgg
 
        return imgDict

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