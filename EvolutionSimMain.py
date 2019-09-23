################################################################################
# Author: Ezra Bartlett
# This file contains the main simulation logic for this project, including the
# primary runloop of the game
################################################################################

import pygame
from Creature import *
import time
from rayMarcher import *

pygame.init()
pygame.font.init()
clock = pygame.time.Clock()
background = [1,22,39]
myfont = pygame.font.SysFont('timesnewromanttf', 15)

screen = pygame.display.set_mode((500, 500))#, pygame.FULLSCREEN)
#screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("EvoSim")
lsit = []

firstCreature = Creature(screen, (50, 50))
food = [food(screen, (100, 100))]

runFlag = True
generation = 0
# Main game loop
secondCounter = 0

testPolygon = [(200,140),(250, 195), (280, 144)]

testBodies = [[(200,140),(250, 195), (280, 144)],[(290,240),(340, 295), (370, 244)]]
testFoods = [(100,100)]

rayStart = (250, 250)
rayDirection = 3

def drawPoly(polygon):
    pygame.draw.polygon(screen, (0, 0, 255), polygon)

while runFlag:
    dtime = clock.tick(60)
    print(clock.get_fps())
    # dtime = time.time()-last_time
    generation += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                runFlag = False
    # print("Generation "+str(generation))
   # for event in pygame.event.get():
    #    if event.type == pygame.QUIT:
    #       pygame.quit()
    #      sys.exit()

    screen.fill(background)
    for poly in testBodies:
        drawPoly(poly)
    for meal in food:
        meal.draw()
    keys = pygame.key.get_pressed()

    foreward = (keys[273])*.2*dtime
    rotation = (keys[275]-keys[276])*.005*dtime

    # Temporary, for testing fitness evolution
    children = []
    mostFit = 99.9
    bestFitness = 9999.9
    # for i in range(0,9):
    #    children.append(Creature(screen))
    #    children[i].copy(firstCreature)
    #    fitness = children[i].fitnessEval()
    #    if(fitness<bestFitness):
    #        bestFitness = fitness
    #        mostFit = i
    # print("Most fit child:")
    # print(mostFit)
    # print(" ")
    # print(children[mostFit].fitnessEval())
    firstCreature.tick(food, dtime)

    #distanceToCircle(firstCreature.position, food[0].position, 10, screen)
    #firstCreature.mutate()
    # firstCreature = children[mostFit]
    # print(pygame.font.get_fonts())
    castRay(rayStart, rayDirection, 100, testFoods, testBodies, screen)
    rayDirection = rayDirection+.01;

    textsurface = myfont.render(
        str(pygame.time.Clock().get_fps()), False, (10, 10, 10))
    # screen.blit(textsurface, (400, 0))

    pygame.display.update()



def main():
    pass


main()
