
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

    def neighbour_coordinates(self, row, column):
        upper_row = (row - 1) % self.height
        bottom_row = (row + 1) % self.height
        left_column = (column - 1) % self.width
        right_column = (column + 1) % self.width
        neighbours = [(upper_row, left_column), (upper_row, column), (upper_row, right_column),
                      (row, left_column), (row, right_column),
                      (bottom_row, left_column), (bottom_row, column), (bottom_row, right_column)]
        return neighbours
