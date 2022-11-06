from dataclasses import dataclass
from enum import Enum
from typing import Any

from iota import iota


class TokenType(Enum):
    LITERAL = iota(True)
    FUNCTION = iota()


@dataclass
class Token:
    __match_args__ = ("type", "value", "text")

    type: TokenType
    value: Any
    text: str

    def __str__(self):
        return f"Token({self.type.name}, {self.value}, \"{self.text}\")"

    def __repr__(self):
        return str(self)
