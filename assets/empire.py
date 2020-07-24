from enum import Enum


class _Empire(object):
    def __init__(self, adjective, capital, name, coordinates):
        self.adjective = adjective
        self.capital = capital
        self.name = name
        self.coordinates = coordinates


class Empire(Enum):
    BRITISH = _Empire("British", 'portroyal', '', (0, 0))
    FRENCH = _Empire("French", 'martinique', '', (0, 0))
    DUTCH = _Empire("Dutch", 'curacao', '', (0, 0))
    SPANISH = _Empire("Spanish", 'havanna', '', (0, 0))
    PIRATE = _Empire("Pirate", 'tortuga', '', (0, 0))

    @classmethod
    def get_by_name(cls, name):
        for empire in cls:
            if empire.value.name == name:
                return empire.value
        raise RuntimeError(f"Invalid empire name: '{name}'")

    @classmethod
    def get_names(cls):
        return [empire.value.name for empire in cls]
