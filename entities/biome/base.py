import abc


class Base(abc.ABC):
    def __init__(self, cell):
        self.cell = cell

    @abc.abstractmethod
    def do_cycle(self):
        pass
