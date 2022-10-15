import math
import random
from cellularworld.world import matrix

MAX_HEIGHT = 16
CHOICE_RANGE = 2**MAX_HEIGHT

SIZE = 40


class Terrain:
    def generate(self):
        terrain = matrix.Matrix(SIZE, SIZE)
        self._randomise(terrain)
        self._smooth(terrain)
        self._descretify(terrain)
        return terrain

    def _descretify(self, terrain):
        for row in range(SIZE):
            for column in range(SIZE):
                terrain[row][column] = round(terrain[row][column])

    def _smooth(self, terrain):
        for row in range(SIZE):
            for column in range(SIZE):
                terrain[row][column] = self._neighbourhood_average(terrain, row, column)

    def _randomise(self, terrain):
        for row in range(SIZE):
            for column in range(SIZE):
                terrain[row][column] = self._generate_height()

    def _neighbourhood_average(self, terrain, row, column):
        average = terrain[row][column]
        neighbour_coordinates = terrain.neighbour_coordinates(row, column)
        for neighbour_row, neighbour_column in neighbour_coordinates:
            average += terrain[neighbour_row][neighbour_column]
        average /= len(neighbour_coordinates)
        return average

    def _generate_height(self):
        randomised_height = random.randint(1, CHOICE_RANGE)
        normalised_height = 16 - math.floor(math.log2(randomised_height))
        return normalised_height
