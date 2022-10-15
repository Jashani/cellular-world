from cellularworld.entities import state, wind
from cellularworld.entities.biome import factory as biome_factory


class Cell:
    def __init__(self, biome_type, height):
        self.state = state.State()
        self.wind = wind.Wind(self, ["mock", "neighbours", "for", "now"])
        self.biome = None
        self.set_biome(biome_type)
        self.height = height

    def set_biome(self, biome_type):
        self.biome = biome_factory.new(biome_type, self)
