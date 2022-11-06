from parser.matcher import Result
from parser.tokens import TokenType, Token


class Action:
    def __call__(self, match):
        return None


class SimpleAction(Action):
    def __init__(self, transformer):
        self.transformer = transformer

    def __call__(self, match):
        return self.transformer(match)


class Entoken(Action):
    def __init__(self, type: TokenType):
        self.type = type

    def __call__(self, match):
        return Token(self.type, match.value, match.text)


class Select(Action):
    def __init__(self, *indices):
        self.indices = indices

    def __call__(self, match):
        values = match.value
        if len(self.indices) == 1:
            return values[self.indices[0]]
        return [v for i, v in enumerate(values) if i in self.indices]


class Map(Action):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __call__(self, match):
        values = match.value
        return {key: values[index] for key, index in self.kwargs.items()}
