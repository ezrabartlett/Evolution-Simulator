################################################################################
# Author: Ezra Bartlett
# This file contains the main simulation logic for this project, including the
# primary runloop of the game
################################################################################

import pygame
from Creature import *

pygame.init()

screen = pygame.display.set_mode((500, 500))

pygame.display.set_caption("EvoSim")
lsit = []

firstCreature = Creature(screen, (50, 50))
food = food(screen, (100, 100))

runFlag = True
generation = 0
# Main game loop
while runFlag:
    generation += 1
    #print("Generation "+str(generation))
    pygame.time.delay(1)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((255, 255, 255))
    food.draw()
    keys = pygame.key.get_pressed()
    for i in range(1, len(keys)):
        if(keys[i] == 1):
            print(i)

    foreward = (keys[273])*10
    rotation = (keys[275]-keys[276])*.1

    firstCreature.manualMove(foreward, rotation)
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

    firstCreature.mutate()

    # firstCreature = children[mostFit]
    firstCreature.draw()

    pygame.display.update()


def main():
    pass


main()
