# import the pygame module, so you can use it
import pickle,pygame,sys
from pygame.locals import *
from random import random, randint
import numpy as np

from constants import *

class Environment():
    def __init__(self, rows=ROWS, columns=COLUMNS):
        self.rows = rows
        self.columns = columns
        self.surface = np.zeros((self.rows, self.columns))

    #getters
    def get_rows(self):
        return self.rows

    def get_columns(self):
        return self.columns

    def get_surface(self):
        return self.surface

    def randomMap(self, fill=0.2):
        for i in range(self.rows):
            for j in range(self.columns):
                if random() <= fill:
                    self.surface[i][j] = 1

    def setEnvirnment(self, rows, columns, surface):
        self.rows = rows
        self.columns = columns
        self.surface = surface

    def __str__(self):
        string = ""
        for i in range(self.rows):
            for j in range(self.columns):
                string = string + str(int(self.surface[i][j]))
            string = string + "\n"
        return string

    def readUDMSensors(self, x, y):
        readings = [0, 0, 0, 0]
        # UP
        xf = x - 1
        while ((xf >= 0) and (self.surface[xf][y] == 0)):
            xf = xf - 1
            readings[UP] = readings[UP] + 1
        # DOWN
        xf = x + 1
        while ((xf < self.rows) and (self.surface[xf][y] == 0)):
            xf = xf + 1
            readings[DOWN] = readings[DOWN] + 1
        # LEFT
        yf = y + 1
        while ((yf < self.columns) and (self.surface[x][yf] == 0)):
            yf = yf + 1
            readings[LEFT] = readings[LEFT] + 1
        # RIGHT
        yf = y - 1
        while ((yf >= 0) and (self.surface[x][yf] == 0)):
            yf = yf - 1
            readings[RIGHT] = readings[RIGHT] + 1

        return readings

    def saveEnvironment(self, numFile):
        with open(numFile, 'wb') as f:
            pickle.dump(self, f)
            f.close()

    def loadEnvironment(self, numfile):
        with open(numfile, "rb") as f:
            dummy = pickle.load(f)
            #self.__rows = dummy.__rows
            #self.__columns = dummy.__columns
            #self.__surface = dummy.__surface
            self.setEnvirnment(dummy.__n, dummy.__m, dummy.__surface)
            f.close()

    def image(self, colour=BLUE, background=WHITE):
        imagine = pygame.Surface((420, 420))
        brick = pygame.Surface((20, 20))
        brick.fill(BLUE)
        imagine.fill(WHITE)
        for i in range(self.rows):
            for j in range(self.columns):
                if (self.surface[i][j] == 1):
                    imagine.blit(brick, (j * 20, i * 20))
        return imagine


class DMap():
    def __init__(self, rows=ROWS, columns=COLUMNS):
        self.__rows = rows
        self.__columns = columns
        self.__surface = np.zeros((self.__rows, self.__columns))
        for i in range(self.__rows):
            for j in range(self.__columns):
                self.__surface[i][j] = -1

    def get_rows(self):
        return self.__rows

    def get_columns(self):
        return self.__columns

    def get_surface(self):
        return self.__surface

    def markDetectedWalls(self, readings, x, y):
        #   To DO
        # mark on this map the walls that you detect and the detected empty spaces
        '''
        :param readings: array returned by e.readUDMSensors() from environment e
                       : saves the number of empty squares until the first wall on directions UP, LEFT, DOWN, RIGHT
                       starting from current position (x,y)
        :param x: coordinate X
        :param y: coordinate Y
        :return: None
        '''
        wals = readings

        #UP
        i = x - 1
        if wals[UP] > 0:
            while ((i >= 0) and (i >= x - wals[UP])):
                self.__surface[i][y] = 0
                i = i - 1
        if (i >= 0):
            self.__surface[i][y] = 1

        #DOWN
        i = x + 1
        if wals[DOWN] > 0:
            while ((i < self.__rows) and (i <= x + wals[DOWN])):
                self.__surface[i][y] = 0
                i = i + 1
        if (i < self.__rows):
            self.__surface[i][y] = 1

        #LEFT
        j = y + 1
        if wals[LEFT] > 0:
            while ((j < self.__columns) and (j <= y + wals[LEFT])):
                self.__surface[x][j] = 0
                j = j + 1
        if (j < self.__columns):
            self.__surface[x][j] = 1

        #RIGHT
        j = y - 1
        if wals[RIGHT] > 0:
            while ((j >= 0) and (j >= y - wals[RIGHT])):
                self.__surface[x][j] = 0
                j = j - 1
        if (j >= 0):
            self.__surface[x][j] = 1

        return None

    def image(self, x, y):
        # draw the board that will be explored by the drone
        imagine = pygame.Surface((420, 420))
        brick = pygame.Surface((20, 20))
        empty = pygame.Surface((20, 20))
        empty.fill(WHITE)
        brick.fill(BLACK)
        imagine.fill(GRAYBLUE)

        for i in range(self.__rows):
            for j in range(self.__columns):
                if (self.__surface[i][j] == 1):
                    imagine.blit(brick, (j * 20, i * 20))
                elif (self.__surface[i][j] == 0):
                    imagine.blit(empty, (j * 20, i * 20))

        drona = pygame.image.load("drona.png")
        imagine.blit(drona, (y * 20, x * 20))
        return imagine

    def validate_position(self, x, y):
        '''
        verifies if drone can move on position (x,y)
        drone cannot move on position if x,y-out of bounds, or (x,y) = wall
        :param x:X coordinate
        :param y:Y coordinate
        :return: boolean
        '''

        # out of bounds
        if x<0 or y<0 or x>=self.__rows or y>=self.__columns:
            return False
        if self.__surface[x][y]==1:
            return False
        return True


class Drone():
    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def move(self, x, y):
        self.__x = x
        self.__y = y
