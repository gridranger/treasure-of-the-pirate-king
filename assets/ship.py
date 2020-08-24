from enum import Enum
from collections import namedtuple


Ship = namedtuple("Ship", ["type", "max_crew", "cost"])


class Ships(Enum):
    GALLEON = Ship("galleon", 10, 0)
    SCHOONER = Ship("schooner", 10, 0)
    BRIGANTINE = Ship("brigantine", 20, 24)
    FRIGATE = Ship("frigate", 36, 56)
