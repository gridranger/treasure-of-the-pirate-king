from enum import Enum


class _Empire(object):
    def __init__(self, adjective, capital, name, coordinates):
        self.adjective = adjective
        self.capital = capital
        self.name = name
        self.coordinates = coordinates


class Empire(Enum):
    BRITISH = _Empire("British", 'Port Royal', '', (0, 0))
    FRENCH = _Empire("French", 'Martinique', '', (0, 0))
    DUTCH = _Empire("Dutch", 'Curacao', '', (0, 0))
    SPANISH = _Empire("Spanish", 'Havanna', '', (0, 0))
    PIRATE = _Empire("Pirate", 'Tortuga', '', (0, 0))

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
    def get_by_adjective(cls, empire_id):
        for empire in cls:
            if empire.value.adjective == empire_id:
                return empire.value
        raise RuntimeError(f"Invalid empire adjective: '{empire_id}'")
