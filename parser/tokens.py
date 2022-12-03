from dataclasses import dataclass
from enum import Enum
from typing import Any


class TokenType(Enum):
    LITERAL = 1
    FUNCTION = 2


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
