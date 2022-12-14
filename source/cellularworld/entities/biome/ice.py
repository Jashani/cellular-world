from cellularworld.entities.biome import base, biome_type
from cellularworld.config import config
import copy

ICE_STAYING_FROZEN_AT = -0


class Ice(base.Base):
    def __init__(self, cell):
        super().__init__(cell)
        self._density = 150  # Default?
        self._future_density = 150

    def __copy__(self):
        cls = self.__class__
        result = cls(self.cell)
        result._density = self._density
        result._future_density = self._future_density
        return result

    @property
    def type(self):
        return biome_type.BiomeType.ICE

    def commit(self):
        self._density = copy.deepcopy(self._future_density)

    def do_cycle(self):
        self.cell.future_state.temperature -= config.effects.biomes.ice.on.heat
        if self.cell.state.temperature > ICE_STAYING_FROZEN_AT:
            self._warm_up()
        else:
            self._cool_down()
        if self._density <= 0:
            self.cell.set_biome(biome_type.BiomeType.SEA)

    def _warm_up(self):
        neighbouring_icebergs = self._neighbouring_icebergs_count()
        neighbourly_love = 1 / (neighbouring_icebergs + 1)
        self._future_density -= self.cell.state.temperature * config.effects.elements.heat.on.ice * neighbourly_love

    def _cool_down(self):
        neighbouring_icebergs = self._neighbouring_icebergs_count()
        neighbourly_love = 1 - (1 / (neighbouring_icebergs + 1))
        added_density = -1 * (self.cell.state.temperature * config.effects.elements.heat.on.ice * neighbourly_love) / self._density
        self._future_density += added_density

    def _neighbouring_icebergs_count(self):
        count = len([neighbour for neighbour in self.cell.neighbours if type(neighbour.biome) == type(self)])
        return count
