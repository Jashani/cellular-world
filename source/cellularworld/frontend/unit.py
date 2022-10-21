import enum


class Unit(enum.Enum):
    def __str__(self):
        return str(self.value)

    TEMPERATURE = u'\u00B0'
    POLLUTION = 'p'
    CLOUD_DENSITY = 'cd'
    WIND = 'mph'


class Direction(enum.Enum):
    def __str__(self):
        return str(self.value)

    NONE = ''
    N = u'\u2191'
    E = u'\u2192'
    S = u'\u2193'
    W = u'\u2190'
    NE = u'\u2197'
    NW = u'\u2196'
    SE = u'\u2198'
    SW = u'\u2199'
