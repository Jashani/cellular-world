import copy
from cellularworld.entities import state, wind
from cellularworld.entities.biome import factory as biome_factory


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

    def set_biome(self, biome_type):
        self.future_biome = biome_factory.new(biome_type, self)

    def do_cycle(self):
        self.pollution_dissipation()
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
