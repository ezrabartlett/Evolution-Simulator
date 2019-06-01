import pygame
from Creature import *


pygame.init()

screen = pygame.display.set_mode((500,500))

pygame.display.set_caption("EvoSim")
lsit = []

firstCreature = Creature(screen)
food = food(screen, (100,100))

runFlag = True
while runFlag:

    pygame.time.delay(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((255,255,255))
    food.draw()

    # Temporary, for testing fitness evolution
    children = []
    mostFit = 99.9
    bestFitness = 9999.9
    print("Children Fitnesses")
    for i in range(0,9):
        print(i)
        children.append(Creature(screen))
        children[i].copy(firstCreature)
        fitness = children[i].fitnessEval()
        if(fitness<bestFitness):
            bestFitness = fitness
            mostFit = i
            print("best fit")
        print(fitness)
    print("chosen")
    print(bestFitness)
    print(mostFit)
    print(children[mostFit].fitnessEval())
    firstCreature = children[mostFit]
    print(firstCreature.fitnessEval())
    firstCreature.draw()


    pygame.display.update()


def main():
    pass

main()
