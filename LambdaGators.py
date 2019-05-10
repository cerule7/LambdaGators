import pygame as pg
import os
import random

def randomColor():
        x = random.randint(10, 240)
        y = random.randint(10, 240)
        z = random.randint(10, 240)

        return (x, y, z)

def render(varList):
        baseColor = (65, 195, 172) #constant value of the base color gator 
        thresh = (0, 0, 0, 0) #threshold value for pygame transform 

        imgDict = {} #dictionary of variables to reference alligator/func or egg/var of variable specific color

        for var in varList:
                imgDict[var] = {} #sub-dictionary per variable
                
                newColor = randomColor() #new random color for new var
                
                tempGator = pg.image.load('Resources/alligator.png') #loads temp Surfaces
                tempEgg = pg.image.load('Resources/egg.png')

                pg.transform.threshold(tempGator, tempGator, baseColor, thresh, newColor, 1, None, True) #makes Surfaces the new var color
                pg.transform.threshold(tempEgg, tempEgg, baseColor, thresh, newColor, 1, None, True) 

                imgDict[var]['alligator'] = tempGator #adds gator and egg to var sub-dict 
                imgDict[var]['egg'] = tempEgg
        
        imgDict["dead"] = pg.image.load('Resources/dead_alligator.png')
        return imgDict

test = ["a" , "b", "c"]
images = render(test)

pg.init()
screen = pg.display.set_mode((1000, 750))
done = False
clock = pg.time.Clock()
 
while not done:
        for event in pg.event.get():
                if event.type == pg.QUIT:
                        done = True
         
        screen.fill((255, 255, 255))

        screen.blit(images["a"]["alligator"], (20, 20))
        screen.blit(images["b"]["egg"], (20, 115))
        screen.blit(images["dead"], (20, 200))
         
        pg.display.flip()
        clock.tick(60)