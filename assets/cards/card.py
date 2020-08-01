from abc import ABC
from settings import ApplicationSettings as s
from .treasurecardtypes import TreasureCardTypes as treasures


class Card(ABC):
    def __init__(self, id):
        self._id = id.value

    @property
    def title(self):
        return s.language.get(f"{self._id}_title")

    @property
    def text(self):
        return s.language.get(f"{self._id}_text")

    @property
    def id(self):
        return self._id

    def __repr__(self):
        return f"{self.__class__.__name__} object at {id(self)}"


class EventCard(Card):
    pass


class TreasureCard(Card):
    pass


class LootCard(TreasureCard):
    _next_loot_id = 0

    def __init__(self, value):
        Card.__init__(self, treasures.treasure)
        self.value = value
        self._loot_id, LootCard._next_loot_id = LootCard._next_loot_id, LootCard._next_loot_id + 1

    @property
    def text(self):
        text = s.language.get(f"{self._id}_text")
        return text.format(self.value)

    @property
    def id(self):
        return f"{self._id}_{self._loot_id}"

    def __repr__(self):
        return f"{self.__class__.__name__} object, value {self.value}, id {self.id} at {id(self)}"
