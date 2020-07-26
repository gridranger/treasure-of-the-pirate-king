from abc import ABC, abstractmethod
from settings import ApplicationSettings as s
from .cardactions import CardActions as actions
from .eventcardtypes import EventCardTypes as events
from .treasurecardtypes import TreasureCardTypes as loots


class Card(ABC):
    def __init__(self, id, event, details=None):
        self._id = id.value
        self._event = event
        self._event_details = details if details else []

    @property
    def title(self):
        return s.language.get(f"{self._id}_title")

    @property
    def text(self):
        return s.language.get(f"{self._id}_text")

    def action(self):
        return self._event, self._event_details


class EventCard(Card):
    pass

class LootCard(Card):
    pass


class Leviathan(EventCard):
    def __init__(self):
        Card.__init__(self, events.leviathan, actions.ADD_PLAYER_STATUS)
        self._event_details = [self._id]


class TreasureCard(LootCard):
    def __init__(self, value):
        Card.__init__(self, loots.treasure, actions.UPDATE_GOLD, [value])
        self.value = value

    @property
    def text(self):
        text = s.language.get(f"{self._id}_text")
        return text.format(self.value)
