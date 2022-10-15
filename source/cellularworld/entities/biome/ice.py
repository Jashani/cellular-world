from cellularworld.entities.biome import base, biome_type


TEMPERATURE_EFFECT_ON_ICE_WEIGHT = 1


class Ice(base.Base):
    def __init__(self, cell):
        super().__init__(cell)
        self._density = 0  # Default?

    @property
    def type(self):
        return biome_type.BiomeType.ICE

    def do_cycle(self):
        self.cell.temperature -= 1  # ICE_EFFECT_ON_TEMPERATURE_WEIGHT
        if self.cell.temperature > 0:
            self._warm_up()
        else:
            self._cool_down()
        if self._density <= 0:
            self.cell.set_biome(biome_type.BiomeType.SEA)

    def _warm_up(self):
        neighbouring_icebergs = self._neighbouring_icebergs_count()
        self._density -= self.cell.temperature * TEMPERATURE_EFFECT_ON_ICE_WEIGHT * (1/(neighbouring_icebergs + 1)) # Multicell but only counting

    def _cool_down(self):
        neighbouring_icebergs = self._neighbouring_icebergs_count()
        self._density += self.cell.temperature * TEMPERATURE_EFFECT_ON_ICE_WEIGHT * (1 - (1/(neighbouring_icebergs + 1))) # Multicell but only counting

    def _neighbouring_icebergs_count(self):
        count = len([neighbour for neighbour in self.cell.neighbours() if type(neighbour.biome) == type(self)])
        return count
