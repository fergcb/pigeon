from parser.matcher import Repeat, Symbol, RegExp
from parser.action import SimpleAction, Entoken, Select

from parser.token import Token


def WS():
    return RegExp("^[ \t\r\n]+")


def NumberLiteral():
    return RegExp(r"^(0|([1-9][0-9]{,2}))") >> SimpleAction(int)


def StringLiteral():
    return RegExp(r"\"((\\.)|[^\"])*\"") \
        >> SimpleAction(lambda s: s[1:-1].encode('utf-8').decode('unicode-escape'))


def Literal():
    return NumberLiteral() | StringLiteral()


def LiteralExpr():
    return Literal() >> Entoken(Token.LITERAL)


def ArrayExpr():
    return Literal() + Repeat(Symbol(",") + Literal() >> Select(1)) \
        >> SimpleAction(lambda l: [l[0], *l[1]]) \
        >> Entoken(Token.LITERAL)


def FunctionExpr():
    return RegExp(r"`?\S") >> Entoken(Token.FUNCTION)


def Expr():
    return ArrayExpr() | LiteralExpr() | FunctionExpr()


def Program():
    return Repeat(Expr())


grammar = Program()
