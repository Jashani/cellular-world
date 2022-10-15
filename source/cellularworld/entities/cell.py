from cellularworld.entities import state, wind
from cellularworld.entities.biome import factory as biome_factory


class Cell:
    def __init__(self, biome_type, height, temperature, pollution, cloud_density):
        self.state = state.State(temperature, pollution, cloud_density)
        self._wind = wind.Wind(self, ["mock", "neighbours", "for", "now"])
        self._biome = None
        self.set_biome(biome_type)
        self.height = height

    def set_biome(self, biome_type):
        self._biome = biome_factory.new(biome_type, self)
