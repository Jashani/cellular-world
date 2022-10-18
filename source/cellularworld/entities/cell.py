import copy
from cellularworld.config import config
from cellularworld.entities import state, wind
from cellularworld.entities.biome import factory as biome_factory
from cellularworld.entities.biome.biome_type import BiomeType


class Cell:
    def __init__(self, biome_type, height):
        self.state = state.State()
        self.wind = wind.Wind(self)
        self.biome = biome_factory.new(biome_type, self)
        self.height = height
        self.neighbours = None

        self.future_state = state.State()
        self.future_wind = wind.Wind(self)
        self.future_biome = biome_factory.new(biome_type, self)

        self.set_temperature()

    def set_biome(self, biome_type):
        self.future_biome = biome_factory.new(biome_type, self)

    def do_cycle(self):
        self.pollution_dissipation()
        self.heat_dissipation()
        self.cool_tall_places()
        self.future_biome.do_cycle()
        self.future_state.do_cycle()
        self.future_wind.do_cycle()

    def commit(self):
        self.future_wind.commit()
        self.future_biome.commit()
        self.state = copy.deepcopy(self.future_state)
        self.biome = copy.deepcopy(self.future_biome)
        self.wind = copy.deepcopy(self.future_wind)
        self.state.validate_values()

    def pollution_dissipation(self):
        self.future_state.pollution = self.future_state.pollution / 9
        for neighbour in self.neighbours:
            self.future_state.pollution += neighbour.state.pollution / 9

    def heat_dissipation(self):
        self.future_state.temperature = self.future_state.temperature / 9
        for neighbour in self.neighbours:
            self.future_state.temperature += neighbour.state.temperature / 9

    def cool_tall_places(self):
        height_value = self.height - config.world.terrain.water_level
        self.future_state.temperature -= height_value * config.effects.elements.height.on.heat

    def set_temperature(self):
        if self.biome.type == BiomeType.ICE:
            self.state.temperature = config.world.start.ice.temperature
        elif self.biome.type == BiomeType.SEA:
            self.state.temperature = config.world.start.sea.temperature
        if self.future_biome.type == BiomeType.ICE:
            self.future_state.temperature = config.world.start.ice.temperature
        elif self.future_biome.type == BiomeType.SEA:
            self.future_state.temperature = config.world.start.sea.temperature
