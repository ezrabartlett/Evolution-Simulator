import pygame
import numpy as np
import math
import random as rand
import NeuralNetwork as nn

class Creature():

    def __init__(self, screen, parent1 = "", parent2 = ""):
        self.screen = screen
        self.pointList = [(rand.random()*500,rand.random()*500),(rand.random()*500,rand.random()*500),(rand.random()*500,rand.random()*500)]

    def copy(self, parent):
        self.pointList = parent.pointList.copy()
        self.mutate()

    def shuffle(self, point):
        randx = rand.random()
        randy = rand.random()

        newx = point[0]+math.log10(randx/(1-randx))*1
        newy = point[1]+math.log10(randy/(1-randy))*1
        #print((newx,newy))
        return (newx,newy)

    def mutate(self):
        for i,point in enumerate(self.pointList):
            tempPoint = self.shuffle(point)
            self.pointList[i] = tempPoint
            self.fitnessEval()
            #if len(self.pointList)>3 and rand.random()<.005:
            #    del self.pointList[i]

            #if rand.random()<.005:
            #    tempPoint = (abs(self.pointList[i-1][0]+point[0])/2,abs(self.pointList[i-1][1]+point[1])/2)
            #    self.pointList.insert(i,tempPoint)

    def fitnessEval(self):
        a = np.array([self.pointList[0][0],self.pointList[0][1]])
        b = np.array([self.pointList[1][0],self.pointList[1][1]])
        c = np.array([self.pointList[2][0],self.pointList[2][1]])

        v1 = b-a
        v2 = c-a

        cosine_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
        angle1 = np.arccos(cosine_angle)

        v1 = a-b
        v2 = c-b

        cosine_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
        angle2 = np.arccos(cosine_angle)

        v1 = b-c
        v2 = a-c

        cosine_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
        angle3 = np.arccos(cosine_angle)

        angles = [angle1*57.2958, angle2*57.2958, angle3*57.2958]
        #print("angles")
        #print(angles)

        fitness = abs(angles[0]-75)+abs(angles[1]-75)+abs(angles[2]-30)#(angles[0]-60)**2+(angles[1]-60)**2+(angles[2]-60)**2
        #print(fitness)
        return fitness

    def draw(self):
        pygame.draw.polygon(self.screen, (0,0,255), self.pointList, 0)
        #self.mutate()

class food():
    def __init__(self, screen, location):
        self.location = location
        self.screen = screen

    def draw(self):
        pygame.draw.circle(self.screen, (0,200,0), (self.location[0], self.location[1]),10)
