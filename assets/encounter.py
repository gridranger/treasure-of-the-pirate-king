from enum import auto
from collections import namedtuple
from extensions import AutoNamedEnum
from .ship import Ships as s
from .empires import Empires as e


class _CannonDamage(AutoNamedEnum):
    MAGAZINE = auto()
    BELOW_WATER_LINE = auto()


c = _CannonDamage

Encounter = namedtuple("Encounter", ["empire", "ship_type", "ship_name", "hits", "loot", "treasure"])

card_encounters = [
    Encounter(e.SPANISH, s.GALLEON, "Trouvadore", (2, 2, c.BELOW_WATER_LINE, 2, 0, c.MAGAZINE), 12, False),
    Encounter(e.SPANISH, s.SCHOONER, "Rosario", (c.BELOW_WATER_LINE, 2, 2, 2, 3, c.MAGAZINE), 16, True),
    Encounter(e.SPANISH, s.BRIGANTINE, "San Lorenzo", (5, c.BELOW_WATER_LINE, 4, 3, 6, c.MAGAZINE), 24, True),
    Encounter(e.SPANISH, s.FRIGATE, "Triunfo", (6, 6, 6, 6, 6, c.MAGAZINE), 32, True),
    Encounter(e.FRENCH, s.GALLEON, "Brézé", (3, 1, 3, 0, c.BELOW_WATER_LINE, c.MAGAZINE), 8, False),
    Encounter(e.FRENCH, s.SCHOONER, "Bougainville", (2, 2, 2, c.BELOW_WATER_LINE, 1, c.MAGAZINE), 8, True),
    Encounter(e.FRENCH, s.BRIGANTINE, "Mutin", (6, 2, c.BELOW_WATER_LINE, 2, 4, c.MAGAZINE), 16, True),
    Encounter(e.FRENCH, s.FRIGATE, "Triomphant", (5, 2, 6, 6, 6, c.MAGAZINE), 32, True),
    Encounter(e.DUTCH, s.GALLEON, "Vogelstruys", (c.BELOW_WATER_LINE, 2, 2, 2, 3, c.MAGAZINE), 16, False),
    Encounter(e.DUTCH, s.SCHOONER, "Eenhoorn", (2, c.BELOW_WATER_LINE, 0, 2, 2, c.MAGAZINE), 8, True),
    Encounter(e.DUTCH, s.BRIGANTINE, "Dolphijn", (3, 3, 3, 3, c.BELOW_WATER_LINE, c.MAGAZINE), 16, True),
    Encounter(e.DUTCH, s.BRIGANTINE, "Triomf", (5, 5, 3, 5, 5, c.MAGAZINE), 24, True),
    Encounter(e.BRITISH, s.GALLEON, "Godspeed", (2, 2, 2, c.BELOW_WATER_LINE, 2, c.MAGAZINE), 8, False),
    Encounter(e.BRITISH, s.SCHOONER, "Royal Will", (4, 0, c.BELOW_WATER_LINE, 0, 4, c.MAGAZINE), 8, True),
    Encounter(e.BRITISH, s.BRIGANTINE, "Victory", (c.BELOW_WATER_LINE, 4, 5, 4, 3, c.MAGAZINE), 16, True),
    Encounter(e.BRITISH, s.FRIGATE, "Triumph", (6, 5, 6, 5, 6, c.MAGAZINE), 32, True),
    Encounter(e.PIRATE, s.SCHOONER, "Pirate0", (2, c.BELOW_WATER_LINE, 2, 4, 2, c.MAGAZINE), 16, False),
    Encounter(e.PIRATE, s.SCHOONER, "Pirate1", (4, 3, 4, 0, c.BELOW_WATER_LINE, c.MAGAZINE), 16, True),
    Encounter(e.PIRATE, s.BRIGANTINE, "Pirate2", (6, 5, 4, c.BELOW_WATER_LINE, 5, c.MAGAZINE), 24, True),
    Encounter(e.PIRATE, s.BRIGANTINE, "Pirate3", (6, 6, 6, 6, 6, 6), 40, False),
]

board_encounters = [
    Encounter(e.FRENCH, s.GALLEON, "Loire", (3, 3, 3, c.BELOW_WATER_LINE, 0, c.MAGAZINE), 8, False),
    Encounter(e.DUTCH, s.SCHOONER, "Hollandia", (3, 0, 3, c.BELOW_WATER_LINE, 2, 3, c.MAGAZINE), 16, False),
    Encounter(e.SPANISH, s.BRIGANTINE, "Almiranta", (0, c.BELOW_WATER_LINE, 5, 5, 4, c.MAGAZINE), 24, False),
    Encounter(e.BRITISH, s.FRIGATE, "Falcon", (5, 4, 6, 6, 2, c.MAGAZINE), 32, False)
]
