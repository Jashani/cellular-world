from cellularworld.entities.biome import base


class Forest(base.Base):

    def do_cycle(self):
        self.cell.state.pollution -= 1  # Configurable
