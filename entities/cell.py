import state
import wind
import biome.factory


class Cell:
    def __init__(self, biome_type, height, temperature, pollution, cloud_density):
        self._state = state.State(height, temperature, pollution, cloud_density)
        self._wind = wind.Wind(self, ["mock", "neighbours", "for", "now"])
        self._biome = None
        self.set_biome(biome_type)

    def set_biome(self, biome_type):
        self._biome = biome.factory.new(biome_type, self)
