from cellularworld.world import matrix, noise

MAX_HEIGHT = 16
HEIGHT_RANGE = (0, MAX_HEIGHT)
EDGE_THICKNESS = 2
LAND_HARSHNESS = 4
SMOOTHING_ITERATIONS = 3

SIZE = 35


class Terrain:
    def generate(self, seed):
        terrain = matrix.Matrix(SIZE, SIZE)
        self._create(terrain, seed)
        for iteration in range(SMOOTHING_ITERATIONS):
            self._smooth_edges(terrain)
        self._descretify(terrain)
        return terrain

    def _descretify(self, terrain):
        for row in range(SIZE):
            for column in range(SIZE):
                terrain[row][column] = round(terrain[row][column])

    def _smooth_edges(self, terrain):
        for edge in self._edges(SIZE):
            for point in range(SIZE):
                row, column = edge, point
                self._smooth(column, row, terrain)
                row, column = point, edge
                self._smooth(column, row, terrain)

    def _smooth(self, column, row, terrain):
        terrain[row][column] = self._neighbourhood_average(terrain, row, column)

    def _create(self, terrain, seed):
        width, height = SIZE, SIZE
        noise_map = noise.Noise.generate(LAND_HARSHNESS, seed, width, height)
        noise_range = noise.Noise.range(noise_map)
        for row in range(height):
            for column in range(width):
                point_value = noise_map[row][column]
                terrain[row][column] = self._linear_interpolation(*noise_range, *HEIGHT_RANGE, point_value)

    def _neighbourhood_average(self, terrain, row, column):
        average = terrain[row][column]
        neighbour_coordinates = terrain.neighbour_coordinates(row, column)
        for neighbour_row, neighbour_column in neighbour_coordinates:
            average += terrain[neighbour_row][neighbour_column]
        average /= len(neighbour_coordinates) + 1
        return average

    def _linear_interpolation(self, from_start, from_end, to_start, to_end, value):
        result = to_start + ((to_end - to_start) / (from_end - from_start)) * (value - from_start)
        return result

    def _edges(self, size):
        full_range = list(range(size))
        edges = full_range[:EDGE_THICKNESS] + full_range[-EDGE_THICKNESS:]
        return edges
