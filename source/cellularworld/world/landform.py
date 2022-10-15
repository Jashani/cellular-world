from cellularworld.world import noise
from cellularworld.entities.biome import biome_type

CITY_THRESHOLD = 11
CITY_SPREAD = 12
FOREST_THRESHOLD = 8
FOREST_SPREAD = 6
ICE_THRESHOLD = 14
ICE_SPREAD = 4


class Landform:
    def populate(self, terrain, seed):
        self._draw_cities(terrain, seed)
        self._draw_forests(terrain, seed)
        self._draw_ice(terrain, seed)

    def _draw_cities(self, terrain, seed):
        self._draw(seed + 1, terrain, biome_type.BiomeType.LAND, biome_type.BiomeType.CITY, CITY_THRESHOLD, CITY_SPREAD)

    def _draw_forests(self, terrain, seed):
        self._draw(seed * 2, terrain, biome_type.BiomeType.LAND, biome_type.BiomeType.FOREST, FOREST_THRESHOLD, FOREST_SPREAD)

    def _draw_ice(self, terrain, seed):
        self._draw(seed * 3, terrain, biome_type.BiomeType.SEA, biome_type.BiomeType.ICE, ICE_THRESHOLD, ICE_SPREAD)

    def _draw(self, seed, terrain, conditional_biome, new_biome_type, threshold, spread):
        biome_map = noise.Noise.generate(spread, seed, terrain.width, terrain.height, 0, 16)
        for row in range(biome_map.height):
            for column in range(biome_map.width):
                if terrain[row][column].biome.type == conditional_biome and biome_map[row][column] >= threshold:
                    terrain[row][column].set_biome(new_biome_type)
