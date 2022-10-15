import base
import biome_type


SEA_FREEZING_THRESHOLD = -5  # Configurable


class Sea(base):

    def do_cycle(self):
        self.cell.state.cloud_density += max(0, self.cell.state.temperature * 1)  # TEMPERATURE_EFFECT_ON_SEA_CLOUD_CREATION_WEIGHT
        if self.cell.state.temperature <= SEA_FREEZING_THRESHOLD:
            self.cell.set_biome(biome_type.BiomeType.ICE)