from cellularworld.entities.biome import base, biome_type


FOREST_POLLUTION_EFFECT = 0.3


class Forest(base.Base):
    @property
    def type(self):
        return biome_type.BiomeType.FOREST

    def do_cycle(self):
        self.cell.future_state.pollution -= FOREST_POLLUTION_EFFECT
