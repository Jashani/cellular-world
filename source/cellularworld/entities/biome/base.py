import abc


class Base(abc.ABC):
    def __init__(self, cell):
        self.cell = cell

    @property
    @abc.abstractmethod
    def type(self):
        pass

    @abc.abstractmethod
    def do_cycle(self):
        pass
