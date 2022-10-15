from cellularworld.entities.biome import base, biome_type


class Land(base.Base):
    @property
    def type(self):
        return biome_type.BiomeType.LAND

    def do_cycle(self):
        pass
