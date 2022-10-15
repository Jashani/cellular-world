from cellularworld.entities.biome import biome_type
from cellularworld.world import matrix, noise
from cellularworld.entities import cell

MAX_HEIGHT = 16
HEIGHT_RANGE = (0, MAX_HEIGHT)
EDGE_THICKNESS = 2
LAND_HARSHNESS = 4
SMOOTHING_ITERATIONS = 3
WATER_LEVEL = 9
SIZE = 35


class Terrain:
    def generate(self, seed):
        height_map = matrix.Matrix(SIZE, SIZE)
        self._create(height_map, seed)
        for iteration in range(SMOOTHING_ITERATIONS):
            self._smooth_edges(height_map)
        self._descretify(height_map)
        terrain = self._generate_cells(height_map)
        return terrain
    
    def _generate_cells(self, height_map):
        terrain = matrix.Matrix(SIZE, SIZE)
        for row in range(height_map.width):
            for column in range(height_map.height):
                height = height_map[row][column]
                biome = self._biome(height)
                terrain[row][column] = cell.Cell(biome, height)
        return terrain

    def _descretify(self, height_map):
        for row in range(height_map.width):
            for column in range(height_map.height):
                height_map[row][column] = round(height_map[row][column])

    def _smooth_edges(self, height_map):
        for row in self._edges(height_map.height):
            for column in range(height_map.width):
                self._smooth(row, column, height_map)

        for column in self._edges(height_map.width):
            for row in range(height_map.height):
                self._smooth(row, column, height_map)

    def _smooth(self, row, column, height_map):
        height_map[row][column] = self._neighbourhood_average(height_map, row, column)

    def _create(self, height_map, seed):
        noise_map = noise.Noise.generate(LAND_HARSHNESS, seed, height_map.width, height_map.height)
        noise_range = noise.Noise.range(noise_map)
        for row in range(height_map.width):
            for column in range(height_map.height):
                point_value = noise_map[row][column]
                height_map[row][column] = self._linear_interpolation(*noise_range, *HEIGHT_RANGE, point_value)

    def _biome(self, height):
        if height <= WATER_LEVEL:
            return biome_type.BiomeType.SEA
        return biome_type.BiomeType.LAND

    def _neighbourhood_average(self, height_map, row, column):
        average = height_map[row][column]
        neighbour_coordinates = height_map.neighbour_coordinates(row, column)
        for neighbour_row, neighbour_column in neighbour_coordinates:
            average += height_map[neighbour_row][neighbour_column]
        average /= len(neighbour_coordinates) + 1
        return average

    def _linear_interpolation(self, from_start, from_end, to_start, to_end, value):
        result = to_start + ((to_end - to_start) / (from_end - from_start)) * (value - from_start)
        return result

    def _edges(self, size):
        full_range = list(range(size))
        edges = full_range[:EDGE_THICKNESS] + full_range[-EDGE_THICKNESS:]
        return edges
