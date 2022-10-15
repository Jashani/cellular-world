import base


class City(base):

    def do_cycle(self):
        self.cell.state.pollution += 1  # Configurable
