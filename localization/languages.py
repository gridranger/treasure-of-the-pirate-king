from enum import Enum
from .english import English
from .hungarian import Hungarian
from .pirate import Pirate


class Languages(Enum):
    ENGLISH = English()
    HUNGARIAN = Hungarian()
    PIRATE = Pirate()

    @classmethod
    def get_language_by_name(cls, name):
        for language in cls:
            if language.value.name == name:
                return language.value
        raise RuntimeError(f"No such language as '{name}'. Available languages are: "
                           f"{', '.join([l.value.name for l in cls])}.")
