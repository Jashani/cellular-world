from cellularworld.entities.biome import base, biome_type


SEA_FREEZING_THRESHOLD = -5  # Configurable
TEMPERATURE_EFFECT_ON_SEA_CLOUD_CREATION_WEIGHT = 0.1


class Sea(base.Base):
    @property
    def type(self):
        return biome_type.BiomeType.SEA

    def do_cycle(self):
        self.cell.future_state.cloud_density += max(0, self.cell.state.temperature * TEMPERATURE_EFFECT_ON_SEA_CLOUD_CREATION_WEIGHT)
        if self.cell.state.temperature <= SEA_FREEZING_THRESHOLD:
            self.cell.set_biome(biome_type.BiomeType.ICE)
