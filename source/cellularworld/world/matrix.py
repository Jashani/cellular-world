
NULL_CHARACTER = 'X'


class Matrix:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self._matrix = []
        for row in range(height):
            self._matrix.append([NULL_CHARACTER] * width)

    @classmethod
    def from_pythonic(cls, matrix):
        height = len(matrix)
        width = len(matrix[0])
        if any([row for row in matrix if len(row) != width]):
            raise Exception(f"Creating matrix from non-matrix: {matrix}")
        new_matrix = cls(width, height)
        for row in range(height):
            for column in range(width):
                new_matrix[row][column] = matrix[row][column]
        return new_matrix

    def __iter__(self):
        return iter(self._matrix)

    def __getitem__(self, row):
        if type(row) is not int:
            raise Exception("Matrix should be accessed with integers")
        return self._matrix[row]

    def __repr__(self):
        return '\n'.join([' '.join([f'{item}' for item in row]) for row in self._matrix])

    def __setitem__(self, key, value):
        raise Exception("Please don't access rows directly :(")

    def apply_to_all(self, method):
        for row in range(self.height):
            for column in range(self.width):
                method(self._matrix[row][column])

    def all_cells(self):
        for row in range(self.height):
            for column in range(self.width):
                yield row, column

    def smooth(self, row, column):
        self[row][column] = self._neighbourhood_average(row, column)

    def neighbour_coordinates(self, row, column):
        upper_row = (row - 1) % self.height
        bottom_row = (row + 1) % self.height
        left_column = (column - 1) % self.width
        right_column = (column + 1) % self.width
        neighbours = [(row, left_column), (bottom_row, left_column), (bottom_row, column), (bottom_row, right_column),
                      (row, right_column), (upper_row, right_column), (upper_row, column), (upper_row, left_column)]
        return neighbours

    def _neighbourhood_average(self, row, column):
        if type(self[row][column]) not in (int, float):
            raise Exception('Only numbers can be averaged :(')
        average = self[row][column]
        neighbour_coordinates = self.neighbour_coordinates(row, column)
        for neighbour_row, neighbour_column in neighbour_coordinates:
            average += self[neighbour_row][neighbour_column]
        average /= len(neighbour_coordinates) + 1
        return average
