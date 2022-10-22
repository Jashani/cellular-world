import perlin_noise
from cellularworld.world import matrix


class Noise:

    @classmethod
    def generate(cls, noise_level, seed, width, height, range_start, range_end):
        noise = perlin_noise.PerlinNoise(octaves=noise_level, seed=seed)
        noise_map = [[noise([row/width, column/height]) for column in range(width)] for row in range(height)]
        noise_map = matrix.Matrix.from_pythonic(noise_map)
        cls._interpolate(noise_map, range_start, range_end)
        return noise_map

    @staticmethod
    def _range(noise_map):
        heights = sum(noise_map, [])
        lowest = min(heights)
        highest = max(heights)
        return lowest, highest

    @classmethod
    def _interpolate(cls, noise_map, range_start, range_end):
        noise_range = cls._range(noise_map)
        for row, column in noise_map.all_cells():
            point_value = noise_map[row][column]
            noise_map[row][column] = cls._linear_interpolation(*noise_range, range_start, range_end, point_value)

    @staticmethod
    def _linear_interpolation(from_start, from_end, to_start, to_end, value):
        result = to_start + ((to_end - to_start) / (from_end - from_start)) * (value - from_start)
        return result
