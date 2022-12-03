from interpreter.block import Block
from parser.matcher import Repeat, Symbol, RegExp, Lazy, EOF
from parser.action import SimpleAction, Entoken, Select

from parser.tokens import TokenType


def WS():
    return RegExp("^[ \t\r\n]+")


def NumberLiteral():
    return RegExp(r"^(0|([1-9][0-9]{,2}))") >> SimpleAction(lambda m: int(m.value))


def StringLiteral():
    return RegExp(r"\"((\\.)|[^\"])*\"") \
        >> SimpleAction(lambda s: s.value[1:-1].encode('utf-8').decode('unicode-escape'))


def BlockLiteral():
    return Symbol("{") + Repeat(Lazy(Expr)) + (Symbol("}") | EOF()) \
        >> Select(1) >> SimpleAction(lambda b: Block(b.value, b.text))


def Literal():
    return NumberLiteral() | StringLiteral() | BlockLiteral()


def LiteralExpr():
    return Literal() >> Entoken(TokenType.LITERAL)


def ArrayExpr():
    return Literal() + Repeat(Symbol(",") + Literal() >> Select(1)) \
        >> SimpleAction(lambda l: [l.value[0], *l.value[1]]) \
        >> Entoken(TokenType.LITERAL)


def FunctionExpr():
    return RegExp(r"`?[^\s{}]") >> Entoken(TokenType.FUNCTION)


def Expr():
    return ArrayExpr() | LiteralExpr() | FunctionExpr()


def Program():
    return Repeat(Expr())


grammar = Program()
