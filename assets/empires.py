from enum import Enum


class Empire(object):
    def __init__(self, adjective, capital, coordinates):
        self.adjective = adjective
        self.capital = capital
        self.coordinates = coordinates


class Empires(Enum):
    BRITISH = Empire("British", 'Port Royal', (0, 0))
    FRENCH = Empire("French", 'Martinique', (0, 0))
    DUTCH = Empire("Dutch", 'Curacao', (0, 0))
    SPANISH = Empire("Spanish", 'Havanna', (0, 0))
    PIRATE = Empire("Pirate", 'Tortuga', (0, 0))

    @classmethod
    def get_by_name(cls, name):
        for empire in cls:
            if empire.value.name == name:
                return empire.value
        raise RuntimeError(f"Invalid empire name: '{name}'")

    @classmethod
    def get_names(cls):
        return [empire.value.name for empire in cls]

    @classmethod
    def get_by_adjective(cls, adjective):
        for empire in cls:
            if empire.value.adjective == adjective:
                return empire.value
        raise RuntimeError(f"Invalid empire adjective: '{adjective}'")
