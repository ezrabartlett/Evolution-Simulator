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
        self.pointList = [(rand.random()*500, rand.random()*500), (rand.random()
                                                                   * 500, rand.random()*500), (rand.random()*500, rand.random()*500)]
        self.position = position
        self.rotation = rotation

        self.body = [(-10, 0), (10, 0), (0, 20)]

        self.center = self.centroid()

    def centroid(self):
        x = [p[0] for p in self.body]
        y = [p[1] for p in self.body]
        return (sum(x) / len(self.body), sum(y) / len(self.body))

    def translate(self, points, angle, position):
        return np.dot(np.array(points)-np.array(self.center), np.array([[np.cos(angle), np.sin(angle)], [-np.sin(angle), np.cos(angle)]]))+self.center+self.position

    def copy(self, parent):
        self.pointList = parent.pointList.copy()
        self.position = parent.position.copy()
        self.rotation = parent.rotation.copy()
        self.body = parent.body.copy()
        self.center = parent.center.copy()
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
            self.fitnessEval()
            if len(self.body) > 3 and rand.random() < .005:
                del self.body[i]

            if rand.random() < .005:
                tempPoint = (
                    abs(self.body[i-1][0]+point[0])/2, abs(self.body[i-1][1]+point[1])/2)
                self.body.insert(i, tempPoint)

        self.center = self.centroid()

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

    def draw(self):
        pygame.draw.circle(self.screen, (0, 200, 0),
                           (self.position[0], self.position[1]), 10)
