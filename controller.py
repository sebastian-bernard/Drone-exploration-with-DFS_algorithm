from domain import *
from time import sleep

class Controller:
    def __init__(self, environment, drone_map, drone):
        self.__environment = environment
        self.__drone_map = drone_map
        self.__drone = drone
        self.__visited = None

    # getters
    def get_environment(self):
        return self.__environment

    def get_drone_map(self):
        return self.__drone_map

    def get_drone(self):
        return self.__drone

    def get_visited(self):
        return self.__visited

    #utils
    def __mark_detected_walls(self):
        walls = self.__environment.readUDMSensors(self.__drone.get_x(), self.__drone.get_y())
        self.__drone_map.markDetectedWalls(walls, self.__drone.get_x(), self.__drone.get_y())

    def dfs_util(self, x,y, visited):
        #mark drone position
        current_position = (x,y)
        visited.add(current_position)
        #
        for direction in v:
            new_x = x + direction[X]
            new_y = y + direction[Y]
            next_position = (new_x,new_y)
            if next_position not in visited:
                if self.__drone_map.validate_position(new_x,new_y):
                    self.__drone.move(new_x,new_y)
                    self.__mark_detected_walls()
                    visited.add(next_position)
                    self.dfs_util(new_x,new_y,visited)

    def moveDFS(self, x, y):
        if self.__visited == None:
            self.__visited = set()

        self.__mark_detected_walls()
        self.dfs_util(x,y, self.__visited)
