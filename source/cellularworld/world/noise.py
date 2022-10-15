import perlin_noise


class Noise:

    @staticmethod
    def generate(noise_level, seed, width, height):
        noise = perlin_noise.PerlinNoise(octaves=noise_level, seed=seed)
        noise_map = [[noise([row/width, column/height]) for column in range(width)] for row in range(height)]
        return noise_map

    @staticmethod
    def range(noise_map):
        heights = sum(noise_map, [])
        lowest = min(heights)
        highest = max(heights)
        return lowest, highest
