import matplotlib.pyplot as plt
import numpy as np
import Point
import time
import os
from operator import attrgetter
from PIL import Image


class AStar:
    def __init__(self, mapImagePath:str, maxIteration=1000000) -> None:
        self.mapImage = np.asarray(Image.open(mapImagePath))
        self.startPoint:Point.Point = None
        self.endPoint:Point.Point = None
        self.openPoints:list[Point.Point] = []
        self.closedPoints:list[Point.Point] = []
        self.path:list[Point.Point] = []
        self.rectangleDimension = 0
        self.MAX_ITERATION = maxIteration
        self.maxDimension = max(self.mapImage.shape)
        self.rectangleDimension = 250000/self.maxDimension**2
        self.startTime = time.time()
        
    
    def getImageArray(self):
        return self.mapImage
    
    def setStartByColor(self, r, g, b):
        self.startPoint = self.getPointByColor(r, g, b)
        self.startPoint.updateCost(0, float('inf'))

    def setEndByColor(self, r, g, b):
        self.endPoint = self.getPointByColor(r, g, b)

    def setEndByCoordinate(self, x, y):
        self.endPoint = Point.Point(x, y, float('inf'), float('inf'))
    
    def compute(self, showFinalPlot=False, filePath:str=None):
        iteration = 0
        currentPoint:Point.Point = None
        self.openPoints.append(self.startPoint)

        while iteration < self.MAX_ITERATION and len(self.openPoints) > 0:
            self.openPoints = sorted(self.openPoints, key=attrgetter('f_cost', 'g_cost'), reverse=True)
            currentPoint = self.openPoints.pop()
            self.closedPoints.append(currentPoint)

            neighbourPoints = self.getNeighbourPoints(currentPoint)

            for neighbourPoint in neighbourPoints:
                if not self.isPointInList(neighbourPoint, self.closedPoints):
                    
                    self.setCost(neighbourPoint, currentPoint)

                    if not self.isPointInList(neighbourPoint, self.openPoints):
                        self.openPoints.append(neighbourPoint)
                        
            if filePath is not None:
                self.drawLists(filePath, iteration)
            if currentPoint.h_cost == 0:
                break
            
            if iteration%100 == 0:
                allpoints = self.mapImage.shape[0] * self.mapImage.shape[1]
                print(f'Time: {round(time.time()-self.startTime, 1)}\t\tIteration: {iteration}\t\t{100/allpoints*iteration}%')

            iteration += 1
        
        if self.isTarget(currentPoint) is not True:
            raise Exception('EndPointNotReachable')
        if iteration == self.MAX_ITERATION:
            raise Exception('MaxIterationReached')

        if showFinalPlot:
            self.drawLists()
            plt.show()

        return iteration

    def getPath(self, drawPath=False):
        bestPoint:Point.Point = self.endPoint

        while bestPoint.g_cost > 1:
            neighbourPoint = self.getNeighbourPoints(bestPoint)
            min_g_Cost = float('inf')
            for p in neighbourPoint:
                if self.isPointInList(p, self.closedPoints):
                    p = self.getPointFromList(p, self.closedPoints)
                    if p.g_cost < min_g_Cost:
                        min_g_Cost = p.g_cost
                        bestPoint = p
            self.path.append(bestPoint)
        
        if drawPath:
            self.drawPath()

        return self.path



        
    def getPointByColor(self, r, g, b):
        x, y = -1, -1
        for idi, i in enumerate(self.mapImage):
            for idj, j in enumerate(i):
                if j[0] == r and j[1] == g and j[2] == b:
                   x = idj
                   y = idi
        return Point.Point(x, y, float('inf'), float('inf'))
    
    def delteFromList(self, point:Point.Point, list:list[Point.Point]):
        if len(list) > 0:
            return [p for p in list if p.x != point.x and p.y != point.y]
        else:
            return []

    def isTarget(self, point:Point.Point):
        if point is None:
            return False
        if point.x == self.endPoint.x and point.y == self.endPoint.y:
            return True 
        else:
            return False

    def getNeighbourPoints(self, point:Point.Point):
        neighbourPoints:list[Point.Point] = []
        for i in np.arange(-1,2,1):
            for j in np.arange(-1,2,1):
                if i != 0 or j != 0:
                    x = point.x+i
                    y = point.y+j
                    neigbourPoint = Point.Point(x,y)
                    if self.isValidPoint(neigbourPoint):
                        if self.isPointInList(neigbourPoint, self.openPoints):
                            pointFromList = self.getPointFromList(neigbourPoint, self.openPoints)
                            neighbourPoints.append(pointFromList)
                        else:
                            neighbourPoints.append(neigbourPoint)
        return neighbourPoints

    def isWall(self, point:Point.Point):
        x = point.x
        y = point.y
        if self.isPointInMap(point) is not True:
            return False
        if self.mapImage[y][x][0] < 128 and self.mapImage[y][x][1] < 128 and self.mapImage[y][x][2] < 128:
            return True
        else:
            return False
        
    def isValidPoint(self, point:Point.Point):
        if point.x >= 0 and point.y >= 0 and not self.isWall(point) and self.isPointInMap(point):
                    if point.x != self.startPoint.x or point.y != self.startPoint.y:
                            return True
    
    def isPointInMap(self, point:Point.Point):
        maxPos = self.mapImage.shape
        if point.x < maxPos[1] and point.y < maxPos[0]:
            return True
        else:
            return False
        
    def isPointInList(self, point:Point.Point, pointList:list[Point.Point]):
        for p in pointList:
            if p == point:
                return True
        return False

    def setCost(self, point:Point.Point, parentPoint:Point.Point):
        point.parentPoint = parentPoint
        h_cost = self.getDistanceBetweenPoints(point, self.endPoint)
        g_cost = self.getDistanceToParent(point) + parentPoint.g_cost
        if point.g_cost > g_cost:
            point.updateCost(g_cost, h_cost)
    
    def getDistanceBetweenPoints(self, pointStart:Point.Point, pointTarget:Point.Point):
        return np.sqrt(np.abs(pointStart.x-pointTarget.x)**2 + np.abs(pointStart.y-pointTarget.y)**2)

    def getDistanceToParent(self, point:Point.Point):
        distance = 1
        distanceDiagonal = 1.4
        if point.x != point.parentPoint.x and point.y != point.parentPoint.y:
            return distanceDiagonal
        else:
            return distance
    
    def getPointFromList(self, point:Point.Point, list:list[Point.Point]):
        selectedPoint:Point.Point = None
        for p in list:
            if p == point:
                selectedPoint = p
                break
        return selectedPoint
    
    def getLowestGCostFromList(pointList:list[Point.Point]):
        pass

    def drawLists(self, path=None, iterations=0):
        plt.rcParams['figure.figsize'] = [12, 8]
        printLabels = False

        if self.maxDimension < 16: printLabels = True
        precision = 2
        fontSmall = 6
        fontBig = 10

        yellow_x = []
        yellow_y = []
        orange_x = []
        orange_y = []

        for point in self.openPoints:
            if printLabels:
                label = f'{round(point.g_cost,precision)}   {round(point.h_cost,precision)}'
                plt.text(point.x, point.y, label, ha='center',va='bottom',fontsize=fontSmall)
                label = f'{round(point.f_cost,precision)}'
                plt.text(point.x, point.y, label, ha='center',va='top',fontsize=fontBig)
            yellow_x.append(point.x)
            yellow_y.append(point.y)

        for point in self.closedPoints:
            if printLabels:
                label = f'{round(point.g_cost,precision)}   {round(point.h_cost,precision)}'
                plt.text(point.x, point.y, label, ha='center',va='bottom',fontsize=fontSmall)
                label = f'{round(point.f_cost,precision)}'
                plt.text(point.x, point.y, label, ha='center',va='top',fontsize=fontBig)
            orange_x.append(point.x)
            orange_y.append(point.y)
        
        plt.scatter(x=orange_x, y=orange_y, c='orange', marker='s', s=self.rectangleDimension)
        plt.scatter(x=yellow_x, y=yellow_y, c='yellow', marker='s', s=self.rectangleDimension)
        plt.imshow(self.mapImage)

        if path is not None:
            self.createFolder(path)
            plt.savefig(f'{path}/{iterations}_Iteration_V2')
            plt.close()


    def drawPath(self):
        x_list = []
        y_list = []

        self.drawLists()

        for p in self.path:
            x_list.append(p.x)
            y_list.append(p.y)
        
        plt.scatter(x=x_list, y=y_list, c='red', marker='s', s=self.rectangleDimension)
        plt.show()
        

    def createFolder(self, path):
        if not os.path.exists(path):
            os.makedirs(path)