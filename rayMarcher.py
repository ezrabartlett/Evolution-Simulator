import pygame
from Creature import *
import time

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
        pygame.draw.circle(screen,(255, 100, 100),(int(step[0]), int(step[1])), max(5,int(stepSize)), 2)
        step = np.array((step[0]+stepSize*np.cos(direction), step[1]+stepSize*np.sin(direction)))
        if stepSize<2:
            pygame.draw.line(screen, (255,255,255),((int(step[0]), int(step[1]))), (int(origin[0]), int(origin[1])))
            pygame.draw.circle(screen, (200, 200, 0), (int(step[0]), int(step[1])), 5)
            return 100
    pygame.draw.line(screen, (255,255,255),((int(step[0]), int(step[1]))), (int(origin[0]), int(origin[1])))
    return 0
