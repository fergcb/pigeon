from enum import Enum
from iota import iota


class Token(Enum):
    LITERAL = iota(True)
    FUNCTION = iota()
    SCOPE = iota()
    REPEAT = iota()
