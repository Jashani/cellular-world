from cellularworld.entities.biome import biome_type
from cellularworld.world import matrix, noise
from cellularworld.entities import cell
from cellularworld.config import config

EDGE_THICKNESS = 2
SMOOTHING_ITERATIONS = 3


class Terrain:
    def generate(self, seed):
        HEIGHT_RANGE = (0, config.world.terrain.max_height)
        height, width = config.world.terrain.size, config.world.terrain.size
        height_map = noise.Noise.generate(config.world.terrain.harshness, seed, width, height, *HEIGHT_RANGE)
        for iteration in range(SMOOTHING_ITERATIONS):
            self._smooth_edges(height_map)
        self._descretify(height_map)
        terrain = self._generate_cells(height_map)
        return terrain
    
    def _generate_cells(self, height_map):
        terrain = matrix.Matrix(config.world.terrain.size, config.world.terrain.size)
        self._create_cells(height_map, terrain)
        self._set_neighbours(height_map, terrain)
        return terrain

    def _set_neighbours(self, height_map, terrain):
        for row in range(height_map.height):
            for column in range(height_map.width):
                neighbours = [terrain[neighbour_row][neighbour_column] for neighbour_row, neighbour_column in
                              terrain.neighbour_coordinates(row, column)]
                terrain[row][column].neighbours = neighbours

    def _create_cells(self, height_map, terrain):
        for row in range(height_map.height):
            for column in range(height_map.width):
                height = height_map[row][column]
                biome = self._biome(height)
                terrain[row][column] = cell.Cell(biome, height)

    def _descretify(self, height_map):
        for row in range(height_map.height):
            for column in range(height_map.width):
                height_map[row][column] = round(height_map[row][column])

    def _smooth_edges(self, height_map):
        for row in self._edges(height_map.height):
            for column in range(height_map.width):
                height_map.smooth(row, column)

        for column in self._edges(height_map.width):
            for row in range(height_map.height):
                height_map.smooth(row, column)

    def _biome(self, height):
        UNDA_DA_SEA = height <= config.world.terrain.water_level
        if UNDA_DA_SEA:
            return biome_type.BiomeType.SEA
        return biome_type.BiomeType.LAND

    def _edges(self, size):
        full_range = list(range(size))
        edges = full_range[:EDGE_THICKNESS] + full_range[-EDGE_THICKNESS:]
        return edges
