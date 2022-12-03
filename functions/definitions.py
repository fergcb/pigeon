import re

from block import Block
from functions.define import define
from stack import Stack

num = int | float


# BLOCK FUNCTIONS

@define("*", "The block %b is executed %a times:")
def repeat(a: int, b: Block, execute: exec):
    for i in range(a):
        execute(b.code, desc=f"Iteration {i+1}/{a}")


@define("v", "The block %b is executed on a fresh stack with %a arguments, and the results are pushed:")
def scope(a: int, b: Block, execute: exec, s: Stack):
    args = s.top(a)
    res = execute(b.code, Stack(args))
    return tuple(res)


@define("?", "The block %b is executed if %a is truthy:")
def if_(a: any, b: Block, execute: exec):
    if a:
        execute(b.code)


@define("/", "The block %b is executed on each element of %a and the previous result. The final result is pushed:")
def reduce(al: list, b: Block, execute: exec):
    last = al[0]
    for a in al[1:]:
        args = [last, a]
        last = execute(b.code, Stack(args))[0]
    return last


@define("\\", "The block %b is executed one each element of %a and the previous result. The results list is pushed:")
def scan(al: list, b: Block, execute: exec):
    out = [al[0]]
    for a in al[1:]:
        args = [out[-1], a]
        res = execute(b.code, Stack(args))
        out.append(res[-1])
    return tuple(out)


@define("w", "The block %a is executed while the element on the top of the stack is truthy:")
def while_(a: Block, execute: exec, s: Stack):
    while len(s) > 0 and s[-1]:
        execute(a.code)


@define("m", "The block %b is mapped over the elements of %b:", vectorize=False)
def map_(al: list, b: Block, execute: exec):
    return [execute(b.code, Stack([a]))[-1] for a in al]


# COMPARISON

@define("=", "1 is pushed if %a == %b, else 0 is pushed.")
def less_than(a: any, b: any) -> int:
    return int(a == b)


@define("<", "1 is pushed if %a < %b, else 0 is pushed.")
def less_than(a: num, b: num) -> int:
    return int(a < b)


@define(">", "1 is pushed if %a > %b, else 0 is pushed.")
def less_than(a: num, b: num) -> int:
    return int(a > b)


@define("<", "1 is pushed if %a is shorter than %b, else 0 is pushed.")
def less_than(a: list, b: list) -> int:
    return int(a < b)


@define(">", "1 is pushed if %a is longer than %b, else 0 is pushed.")
def less_than(a: list, b: list) -> int:
    return int(a > b)


@define("[", "The smallest element of %a is pushed.")
def min_(a: list) -> any:
    return min(a)


@define("[", "The smallest %b elements of %b are pushed.")
def min_(a: list, b: int) -> any:
    return sorted(a)[:b]


@define("]", "The greatest element of %b is pushed.")
def min_(a: list) -> any:
    return max(a)


@define("]", "The greatest %b elements of %b are pushed.")
def min_(a: list, b: int) -> any:
    return sorted(a)[-b:]


# STRING FUNCTIONS

@define("+", "%a and %b are appended as strings.")
def concat(a: str, b: any) -> str:
    return a + str(b)


@define("+", "%a and %b are appended as strings.")
def concat(a: any, b: str) -> str:
    return str(a) + b


@define("-", "%b is removed from %a.")
def remove(a: str, b: str) -> str:
    return a.replace(b, "")


@define("j", "The elements of %a are joined on %b.")
def join(al: list, b: str) -> str:
    return b.join(map(str, al))


@define("o", "%a is decoded into ascii code point(s).")
def ordinal(a: str) -> int | list[int]:
    return ord(a) if len(a) == 1 else [ord(c) for c in a]


@define("F", "%a is split on whitespace.")
def fields(a: str) -> list[str]:
    return re.split(r"\s", a)


@define("p", "%a is padded on both sides with spaces to be %b chars long.")
def pad(a: str, b: int) -> str:
    return a.center(b, " ")


@define("*", "%a is repeated %b times.")
def pad(a: str, b: int) -> str:
    return a * b


# TYPE CASTING

@define("`l", "%a is cast to a list.")
def to_list(a: str) -> list:
    return list(a)


@define("`s", "%a is cast to a string.")
def to_string(a: any) -> str:
    return str(a)


@define("`n", "%a is cast to an integer.")
def to_int(a: str) -> int:
    return int(a)


@define("`n", "%a is cast to an integer.")
def to_int(a: num) -> int:
    return int(a)


@define("`f", "%a is cast to a float.")
def to_float(a: str) -> float:
    return float(a)


@define("`f", "%a is cast to a float.")
def to_float(a: num) -> float:
    return float(a)


# LIST FUNCTIONS

@define("^", "A list of integers from 0 to %a is pushed.")
def range_(a: int) -> list:
    return list(range(a))


@define("u", "Each item of %a is pushed.")
def unwrap(a: list) -> tuple:
    return tuple(a)


@define("e", "A list of %a items popped from the stack is pushed.")
def enlist(a: int, s: Stack) -> list:
    return list(reversed([s.pop() for _ in range(a)]))


@define("i", "The %bth item of %a is pushed.")
def index(al: list, b: int) -> any:
    return al[b]


@define("i", "A list of elements from %a corresponding to indexes in %b is pushed.")
def index(al: list, bl: list) -> list:
    return [al[b] for b in bl]


@define("@", "The index of each item of %b in %a is pushed.")
def index_of(al: list, bl: list) -> any:
    return [al.index(b) for b in bl]


@define("@", "The index of %b in %a is pushed.")
def index_of(al: list, b: any) -> any:
    return al.index(b)


@define("p", "%a is split into %b-item chunks.")
def partition(al: list, b: int) -> list:
    return [al[i:i + b] for i in range(0, len(al), b)]


@define("/", "%a is split into chunks delimited by %b.")
def split(a: list, b: any) -> list:
    groups = []
    group = []
    for el in a:
        if el == b:
            groups.append(group)
            group = []
        else:
            group.append(el)
    groups.append(group)
    return groups


@define("/", "%a is split into chunks delimited by %b.")
def split(a: str, b: any) -> list:
    return a.split(str(b))


@define("U", "The union of %a and %b is pushed.")
def union(al: list, bl: list) -> list:
    return [a for a in al if a in bl]


@define("N", "The difference of %a and %b is pushed.")
def union(al: list, bl: list) -> list:
    return [a for a in al if a not in bl]


@define("N", "All instances of %b are removed from %a.")
def difference(al: list, b: any) -> list:
    return [a for a in al if a != b]


@define("z", "%a is zipped with %b.")
def zip_(a: list | str, b: list | str) -> list:
    return [list(x) for x in zip(a, b)]


@define("*", "%a is repeated %b times.")
def pad(a: list, b: int) -> list:
    return a * b


# CONSTANTS

@define("b", "The list [0, 1] is pushed.")
def bits() -> list:
    return [0, 1]


@define("E", "The empty string is pushed.")
def empty_string() -> str:
    return ""


@define("n", "The newline character, \"\n\", is pushed.")
def newline() -> str:
    return "\n"


@define("s", "A space, \" \", is pushed.")
def space() -> str:
    return " "


# STACK MANIPULATION

@define(":", "A copy of the %ta %a is pushed.", vectorize=False)
def duplicate(a: any) -> tuple:
    return a, a


@define("`:", "A copy each of the %ta %a and the %tb %b are pushed.", vectorize=False)
def dup_two(a: any, b: any) -> tuple:
    return a, b, a, b


@define("c", "The %ta %a and the %tb %b are swapped.", vectorize=False)
def cycle(a: any, b: any) -> tuple:
    return b, a


@define("r", "The %ta %a is moved to the bottom of the stack.", vectorize=False)
def rotate(a: any, s: Stack):
    s.insert(0, a)


@define("#", "The %ta %a is discarded.")
def void(_: any):
    pass


# INPUT / OUTPUT

@define(".", "The %ta %a is printed to the console.", vectorize=False)
def print_(a: any):
    print(a)


@define("`d", "The contents of the stack is printed.")
def dump(s: Stack):
    print(s)


@define(",", "An input value is pushed.")
def input_():
    return input()


@define(";", "An integer input is pushed.")
def input_():
    return int(input())


# ELEMENT_WISE MATHS

@define("+", "The element-wise sums of %a and %b are pushed.")
def sum_items(al: list, bl: list):
    return [a + b for a, b in zip(al, bl)]


@define("-", "The element-wise differences of %a and %b are pushed.")
def subtract_items(al: list, bl: list) -> list:
    return [a - b for a, b in zip(al, bl)]


@define("*", "The element-wise products of %a and %b are pushed.")
def multiply_items(al: list, bl: list) -> list:
    return [a * b for a, b in zip(al, bl)]


@define("/", "The element-wise quotients of %a and %b are pushed.")
def divide_items(al: list, bl: list) -> list:
    return [a / b for a, b in zip(al, bl)]


@define("%", "The element-wise modulus of %a and %b are pushed.")
def modulo_items(al: list, bl: list) -> list:
    return [a / b for a, b in zip(al, bl)]


# MATHS

@define("+", "%a+%b is pushed.")
def add(a: num, b: num) -> num:
    return a + b


@define("-", "%a-%b is pushed.")
def subtract(a: num, b: num) -> num:
    return a - b


@define("*", "%a×%b is pushed.")
def multiply(a: num, b: num) -> num:
    return a * b


@define("/", "%a÷%b is pushed.")
def divide(a: num, b: num) -> num:
    return a / b


@define("%", "%a%%b is pushed.")
def modulo(a: num, b: num) -> num:
    return a % b


# ELEMENT-WISE LOGIC

@define("&", "The element-wise ANDs of %a and %b are pushed.")
def and_items(al: list, bl: list) -> list:
    return [a and b for a, b in zip(al, bl)]


@define("|", "The element-wise ORs of %a and %b are pushed.")
def or_items(al: list, bl: list) -> list:
    return [a or b for a, b in zip(al, bl)]


# LOGIC

@define("&", "The short-circuiting AND of %a and %b is pushed.")
def and_(a: any, b: any) -> any:
    return a and b


@define("|", "The short-circuiting OR of %a and %b is pushed.")
def or_(a: any, b: any) -> any:
    return a or b


@define("t", "1 is pushed if the %ta %a is truthy, else 0 is pushed.")
def truthy(a: any) -> int:
    return int(not not a)


@define("f", "1 is pushed if the %ta %a is falsy, else 0 is pushed.")
def falsy(a: any) -> int:
    return int(not a)
