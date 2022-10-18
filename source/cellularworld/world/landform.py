from cellularworld.world import noise
from cellularworld.entities.biome import biome_type
from cellularworld.config import config


class Landform:
    def populate(self, terrain, seed):
        self._draw_cities(terrain, seed)
        self._draw_forests(terrain, seed)
        self._draw_ice(terrain, seed)

    def _draw_cities(self, terrain, seed):
        self._draw(seed + 1, terrain, biome_type.BiomeType.LAND, biome_type.BiomeType.CITY,
                   config.world.biomes.city.threshold, config.world.biomes.city.spread)

    def _draw_forests(self, terrain, seed):
        self._draw(seed * 2, terrain, biome_type.BiomeType.LAND, biome_type.BiomeType.FOREST,
                   config.world.biomes.forest.threshold, config.world.biomes.forest.spread)

    def _draw_ice(self, terrain, seed):
        self._draw(seed * 3, terrain, biome_type.BiomeType.SEA, biome_type.BiomeType.ICE,
                   config.world.biomes.ice.threshold, config.world.biomes.ice.spread)

    def _draw(self, seed, terrain, conditional_biome, new_biome_type, threshold, spread):
        biome_map = noise.Noise.generate(spread, seed, terrain.width, terrain.height, 0, 16)
        for row in range(biome_map.height):
            for column in range(biome_map.width):
                if terrain[row][column].biome.type == conditional_biome and biome_map[row][column] >= threshold:
                    terrain[row][column].set_biome(new_biome_type)
                    terrain[row][column].set_temperature()
