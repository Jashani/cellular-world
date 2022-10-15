from cellularworld.entities.biome import base


class City(base.Base):

    def do_cycle(self):
        self.cell.state.pollution += 1  # Configurable
