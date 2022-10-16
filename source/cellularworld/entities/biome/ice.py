from cellularworld.entities.biome import base, biome_type


TEMPERATURE_EFFECT_ON_ICE_WEIGHT = 1
ICE_EFFECT_ON_TEMPERATURE_WEIGHT = 1
ICE_STAYING_FROZEN_AT = -0


class Ice(base.Base):
    def __init__(self, cell):
        super().__init__(cell)
        self._density = 1  # Default?
        self._future_density = 1

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
        self.cell.future_state.temperature -= ICE_EFFECT_ON_TEMPERATURE_WEIGHT
        if self.cell.state.temperature > ICE_STAYING_FROZEN_AT:
            self._warm_up()
        else:
            self._cool_down()
        if self._density <= 0:
            self.cell.set_biome(biome_type.BiomeType.SEA)

    def _warm_up(self):
        neighbouring_icebergs = self._neighbouring_icebergs_count()
        self._future_density -= self.cell.state.temperature * TEMPERATURE_EFFECT_ON_ICE_WEIGHT * (1/(neighbouring_icebergs + 1))

    def _cool_down(self):
        neighbouring_icebergs = self._neighbouring_icebergs_count()
        self._future_density += self.cell.state.temperature * TEMPERATURE_EFFECT_ON_ICE_WEIGHT * (1 - (1/(neighbouring_icebergs + 1)))

    def _neighbouring_icebergs_count(self):
        count = len([neighbour for neighbour in self.cell.neighbours if type(neighbour.biome) == type(self)])
        return count
