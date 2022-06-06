import copy
import csv
from typing import Tuple
import pygame


def isNotWall(arr, t: Tuple):
    return not (arr[t[0]][t[1]] == "#" or arr[t[0]][t[1]] == "x")


class Map():
    def __init__(self, file_name):
        self.file_name = file_name
        self.arr = []
        self.start = None
        self.end = None

    def preProcessLevel(self):

        loc_arr = copy.deepcopy(self.arr)
        for x in range(len(loc_arr)):
            for y in range(len(loc_arr[0])):
                tup = (y*40, x*40)
                if loc_arr[x][y] == '':
                    loc_arr[x][y] = ('ground', tup)
                elif loc_arr[x][y] == '#':
                    loc_arr[x][y] = ('wall', tup)
                elif self.arr[x][y] == 'x':
                    loc_arr[x][y] = ('outer_wall', tup)
                elif self.arr[x][y] == 'p':
                    loc_arr[x][y] = ('player', tup)
                elif self.arr[x][y] == 'm':
                    loc_arr[x][y] = ('melee_e', tup)
                elif self.arr[x][y] == 's':
                    loc_arr[x][y] = ('shooting_e', tup)
                elif self.arr[x][y] == 'M':
                    loc_arr[x][y] = ('big_melee_e', tup)
                elif self.arr[x][y] == 'S':
                    loc_arr[x][y] = ('big_shooting_e', tup)
                elif self.arr[x][y] == 'z':
                    loc_arr[x][y] = ('end', tup)
        return loc_arr

    # def __str__(self):
    #     s = '_____________\n'
    #     for x in self.arr:
    #         for y in x:
    #             s += y
    #         s += '\n'
    #     s += '_____________\n'
    #     return s

    def check_key_points(self):

        for x in range(18):
            for y in range(32):
                if self.arr[x][y] == 'p':
                    if self.start is not None:
                        return Exception("too many start points")
                    self.start = (x, y)
                if self.arr[x][y] == 'z':
                    if self.end is not None:
                        return Exception("too many end points")
                    self.end = (x, y)
        if self.start is None:
            return Exception('no starting point')
        if self.end is None:
            return Exception('no end point')
        return None

    def check_path(self):
        err = self.check_key_points()
        if err is not None:
            return err

        loc_arr = copy.deepcopy(self.arr)

        done_cells = []
        next_cells = [self.start]

        while len(next_cells) != 0:
            for e in next_cells:
                if e == self.end:
                    return None

                neighbours = [(-1, 0), (1, 0), (0, 1), (0, -1)]
                element_neighbours = [(e[0] + x, e[1] + y)
                                      for x, y in neighbours]
                for a, b in element_neighbours:
                    try:
                        if loc_arr[a][b] != 2 and isNotWall(loc_arr, (a, b)):
                            loc_arr[a][b] = 1
                            next_cells.append((a, b))
                    except IndexError:
                        pass
                    loc_arr[e[0]][e[1]] = 2
                done_cells.append(e)
                next_cells.remove(e)

        return Exception("no path found")

    def parse_level_csv(self):
        try:
            with open(self.file_name, newline="", mode="r") as csvfile:
                lvl = csv.reader(csvfile, dialect="excel")
                for row in lvl:
                    self.arr.append(row[0].split(";"))
        except Exception as err:
            return err

        return None

    def check_level(self):

        # if the csv has too few lines raise and error or if the walls of the level are not complete
        if len(self.arr) != 18:
            return Exception("too few rows")
        else:
            try:
                for x in range(18):
                    for y in range(32):
                        if x == 0 or y == 0 or x == 17 or y == 31:
                            if self.arr[x][y] != "x":
                                return Exception("invalid wall")
            except IndexError as e:
                return e
        return self.check_path()
