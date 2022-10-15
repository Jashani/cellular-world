from cellularworld.entities.biome import base, biome_type


class Forest(base.Base):
    @property
    def type(self):
        return biome_type.BiomeType.FOREST

    def do_cycle(self):
        self.cell.state.pollution -= 1  # Configurable
