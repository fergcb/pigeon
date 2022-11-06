from dataclasses import dataclass

from parser.tokens import Token


@dataclass
class Block:
    code: list[Token]
    source: str

    def __str__(self):
        return self.source

    def __repr__(self):
        return str(self)
