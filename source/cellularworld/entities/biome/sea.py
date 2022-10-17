from cellularworld.entities.biome import base, biome_type
from cellularworld.config import config


class Sea(base.Base):
    @property
    def type(self):
        return biome_type.BiomeType.SEA

    def do_cycle(self):
        self.cell.future_state.cloud_density += max(0, self.cell.state.temperature * config.effects.elements.heat.on.cloud_creation)
        if self.cell.state.temperature <= config.thresholds.biomes.sea.freezing:
            self.cell.set_biome(biome_type.BiomeType.ICE)
