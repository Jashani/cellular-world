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

    def commit(self):
        pass

    def __copy__(self):
        cls = self.__class__
        result = cls(self.cell)
        return result

    def __deepcopy__(self, memo):
        return self.__copy__()
