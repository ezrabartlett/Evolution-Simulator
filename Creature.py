################################################################################
# Author: Ezra Bartlett
# This file contains the "creature" that will be the star of this simulation
################################################################################

import pygame
import numpy as np
import math
import random as rand
import NeuralNetwork as nn

class Creature():
    """
    A class used to represent a Creature (I'll come up with a better name eventually)

    Attributes
    ----------
    screen :
        The pygame screen that the creature should render to
    pointList : [(x,y),...]
        The points that make up the shape of the creature.

    Methods
    -------
    __init__(self, screen, parent1 = "", parent2 = ""):
        Assigns the screen and accepts the parents, for future sexual style
        selection.

    copy(self, parent):
        Creates a mutated copy of the parent.
    shuffle(self, point):
        Shuffles a point by a random amount. Uses the percent point function,
        in which large deviations have a lower chance of happening

    mutate(self):
        Mutates each point of the shape, with a small chance of adding new points

    fitnessEval(self):
        For determining the fitness of a child creature. Will be useless eventually,
        If natural selection is effectively simulated
    """

    def __init__(self, screen, position=(0, 0), rotation=0, parent1="", parent2=""):
        self.screen = screen
        self.pointList = [(rand.random()*500, rand.random()*500), (rand.random() * 500, rand.random()*500), (rand.random()*500, rand.random()*500)]
        self.position = position
        self.rotation = rotation
        self.resolution = 10
        self.energy = 100
        self.range = 200
        self.maxSpeed = .6
        self.maxAngle = .015
        self.span = 3.14/2
        self.vision = [None] * self.resolution
        self.body = [(-10, 0), (10, 0), (0, 20)]
        self.brain = nn.NeuralNetwork([self.resolution, 5, 2])
        self.center = self.centroid()

    # Will contain the logic to be executed every tick, or every few ticks
    def tick(self, food, dtime):
        self.look(food)
        self.movements = self.brain.forwardProp(self.vision)
        #print(self.movements)
        self.manualMove(self.maxSpeed*self.movements[0][0], self.maxAngle*(self.movements[1][0]-.5)*20*self.maxAngle*dtime)
        self.draw()


    def checkCollision(self, position, collisionList):
        for object in collisionList:
            if (np.linalg.norm((np.array(position) - np.array(object.position))) < 10):
                return 1
        return 0

    def march(self, position, angle, maxDistance, collisionList):
        dMarch = 10
        dx = dMarch*np.cos(angle)
        dy = dMarch*np.sin(angle)

        for i in range(0, int(maxDistance/dMarch)):
            collision = self.checkCollision(position, collisionList)
            if collision != 0:
                pygame.draw.circle(self.screen, (0, 0, 200), (int(position[0]), int(position[1])), 2)
                return collision
            position = (position[0]+dx, position[1]+dy)

        pygame.draw.circle(self.screen, (200, 0, 0), (int(position[0]), int(position[1])), 2)
        return collision
        # returns the color of what it hits, or 0 if nothing is hit.

    # Uses ray tracing to populate the vision array. This will be used as input to the neural net
    def look(self, collisionList):
        center = self.position+self.center
        dangle = self.span/self.resolution
        startingAngle = self.rotation-self.span/2

        for i in range(0, self.resolution):
            self.vision[i] = self.march(self.position, startingAngle+3.14/2+dangle*i, self.range, collisionList)
        #print(self.vision)


    def centroid(self):
        x = [p[0] for p in self.body]
        y = [p[1] for p in self.body]
        return (sum(x) / len(self.body), sum(y) / len(self.body))

    def translate(self, points, angle, position):
        return np.dot(np.array(points)-np.array(self.center), np.array([[np.cos(angle), np.sin(angle)], [-np.sin(angle), np.cos(angle)]]))+self.position

    def copy(self, parent):
        self.pointList = parent.pointList.copy()
        self.position = parent.position.copy()
        self.rotation = parent.rotation.copy()
        self.body = parent.body.copy()
        self.center = parent.center.copy()
        self.resolution = parent.resolution.copy()
        self.span = parent.span.copy()
        self.vision = [None]*self.resolution
        self.brain.copy(parent.brain)
        self.mutate()

    def shuffle(self, point):
        randx = rand.random()
        randy = rand.random()

        newx = point[0]+math.log10(randx/(1-randx))*1
        newy = point[1]+math.log10(randy/(1-randy))*1
        # print((newx,newy))
        return (newx, newy)

    def mutate(self):
        for i, point in enumerate(self.body):
            tempPoint = self.shuffle(point)
            self.body[i] = tempPoint
            #self.fitnessEval()
            if len(self.body) > 3 and rand.random() < .005:
                del self.body[i]

            if rand.random() < .005:
                tempPoint = (
                    abs(self.body[i-1][0]+point[0])/2, abs(self.body[i-1][1]+point[1])/2)
                self.body.insert(i, tempPoint)

        self.center = self.centroid()

    def foodFitnessEval(self, foodList):
        shortestDistance = 9999
        for food in foodList:
            maxDistance = np.linalg.norm(np.array(self.position)-np.array(food.position))
            if(maxDistance<shortestDistance):
                shortestDistance = maxDistance
        return 1/(shortestDistance+.001)

    def fitnessEval(self):
        a = np.array([self.pointList[0][0], self.pointList[0][1]])
        b = np.array([self.pointList[1][0], self.pointList[1][1]])
        c = np.array([self.pointList[2][0], self.pointList[2][1]])

        v1 = b-a
        v2 = c-a

        cosine_angle = np.dot(v1, v2) / \
            (np.linalg.norm(v1) * np.linalg.norm(v2))
        angle1 = np.arccos(cosine_angle)

        v1 = a-b
        v2 = c-b

        cosine_angle = np.dot(v1, v2) / \
            (np.linalg.norm(v1) * np.linalg.norm(v2))
        angle2 = np.arccos(cosine_angle)

        v1 = b-c
        v2 = a-c

        cosine_angle = np.dot(v1, v2) / \
            (np.linalg.norm(v1) * np.linalg.norm(v2))
        angle3 = np.arccos(cosine_angle)

        angles = [angle1*57.2958, angle2*57.2958, angle3*57.2958]
        # print("angles")
        # print(angles)

        # (angles[0]-60)**2+(angles[1]-60)**2+(angles[2]-60)**2
        fitness = abs(angles[0]-75)+abs(angles[1]-75)+abs(angles[2]-30)

        if len(self.pointList) != 3:
            fitness += abs(len(self.pointList)-3)*10

        # print(fitness)
        return fitness

    def draw(self):
        pygame.draw.polygon(self.screen, (0, 0, 255), self.translate(
            self.body, self.rotation, self.position))
        # self.mutate()

    def manualMove(self, foreward, angle):
        self.rotation += angle
        newPosition = (self.position[0]+foreward*np.sin(-self.rotation),
                       self.position[1]+foreward*np.cos(-self.rotation))
        self.position = newPosition


class food():
    def __init__(self, screen, position):
        self.position = position
        self.screen = screen
        self.color = (0, 200, 0)

    def draw(self):
        pygame.draw.circle(self.screen, (0, 200, 0), (self.position[0], self.position[1]), 10)

def distanceToPolygon(point, p2, screen):
    closest = np.linalg.norm((np.array(p2[0])-np.array(point)));
    closestP = 0
    for index,p in enumerate(p2):
        dist = np.linalg.norm((np.array(p)-np.array(point)))
        #print(p)
        if(dist<closest):
            closest = dist
            closestP = index
    index1 = closestP-1;
    index2 = closestP+1;
    index1 = closestP-1;
    if(index1<0):
        index1 = len(p2)-1
    if(index2>=len(p2)):
        index2 = 0
    segpv = np.array(p2[closestP])
    segpw1 = np.array(p2[index1])
    segpw2 = np.array(p2[index2])

    pointVec = np.array(point)
    seg1 = np.linalg.norm(segpv-segpw1)**2
    seg2 = np.linalg.norm(segpv-segpw2)**2

    t1 = max(0, min(1, np.dot((pointVec - segpv), (segpw1 - segpv)) / seg1))
    t2 = max(0, min(1, np.dot((pointVec - segpv), (segpw2 - segpv)) / seg2))

    projection1 = segpv + t1 * (segpw1 - segpv)
    projection2 = segpv + t2 * (segpw2 - segpv)

    closest =  min(np.linalg.norm(pointVec - projection2), np.linalg.norm(pointVec - projection1))

    #pygame.draw.circle(screen, (0,0,100), (int(point[0]),int(point[1])), int(closest))
    #pygame.draw.circle(screen, (0,0,100), (int(segpv[0]),int(segpv[1])), 2)

    #pygame.draw.circle(screen, (0,100,0), (int(segpw1[0]),int(segpw1[1])), 2)
    #pygame.draw.circle(screen, (0,100,0), (int(segpw2[0]),int(segpw2[1])), 2)

    #pygame.draw.circle(screen, (100,0,0), (int(projection1[0]),int(projection1[1])), 2)
    #pygame.draw.circle(screen, (100,0,0), (int(projection2[0]),int(projection2[1])), 2)

    return closest

def distanceToCircle(point, center, radius, screen):
    distance = np.linalg.norm(np.array(point)-np.array(center))-radius
    #pygame.draw.circle(screen, (0, 200, 0), (int(point[0]), int(point[1])), int(distance))
    return distance

def castRay(origin, direction, maxDistance, foods, bodies, screen):
    origin = np.array(origin)
    step = np.array(origin.copy())
    while(np.linalg.norm(step-origin)<maxDistance):
        minDistance = 999999
        for food in foods:
            dist = distanceToCircle(step, food, 10, screen)
            if dist<minDistance:
                minDistance = dist
        for body in bodies:
            dist = distanceToPolygon(step, body, screen)
            if dist<minDistance:
                minDistance = dist
        stepSize = minDistance
        print(stepSize)
        pygame.draw.circle(screen,(255, 100, 100),(int(step[0]), int(step[1])), max(5,int(stepSize)), 2)
        step = np.array((step[0]+stepSize*np.cos(direction), step[1]+stepSize*np.sin(direction)))
        if stepSize<2:
            pygame.draw.line(screen, (255,255,255),((int(step[0]), int(step[1]))), (int(origin[0]), int(origin[1])))
            pygame.draw.circle(screen, (200, 200, 0), (int(step[0]), int(step[1])), 5)
            return 100
    pygame.draw.line(screen, (255,255,255),((int(step[0]), int(step[1]))), (int(origin[0]), int(origin[1])))
    return 0
