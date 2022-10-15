import base


class Forest(base):

    def do_cycle(self):
        self.cell.state.pollution -= 1  # Configurable
