from parser.grammar import grammar
from parser.matcher import Fail


def parse(source):
    match, rest = grammar(source)

    if match is Fail:
        col = len(source) - len(rest)
        raise Exception(f"No match found at col {col}.")

    if rest != "":
        col = len(source) - len(rest)
        raise Exception(f"Expected end of string, found '{rest[:1]}' at col {col}.")

    tokens = match.value

    return tokens
