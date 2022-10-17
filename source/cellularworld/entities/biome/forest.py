from cellularworld.entities.biome import base, biome_type
from cellularworld.config import config


class Forest(base.Base):
    @property
    def type(self):
        return biome_type.BiomeType.FOREST

    def do_cycle(self):
        self.cell.future_state.pollution -= config.effects.biomes.forest.on.pollution
