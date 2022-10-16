from cellularworld.entities.biome import base, biome_type


CITY_POLLUTION_EFFECT = 2.


class City(base.Base):
    @property
    def type(self):
        return biome_type.BiomeType.CITY

    def do_cycle(self):
        self.cell.future_state.pollution += CITY_POLLUTION_EFFECT
