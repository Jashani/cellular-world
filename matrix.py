
NULL_CHARACTER = 'X'


class Matrix:
    def __init__(self, width, height):
        self._matrix = []
        for row in range(height):
            self._matrix.append([NULL_CHARACTER] * width)

    def __getitem__(self, row):
        if type(row) is not int:
            raise Exception("Matrix should be accessed with integers")
        return self._matrix[row]

    def __repr__(self):
        return '\n'.join([' '.join([f'{item}' for item in row]) for row in self._matrix])

    def __setitem__(self, key, value):
        raise Exception("Please don't access rows directly :(")
