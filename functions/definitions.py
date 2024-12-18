import itertools
import re
from functools import cmp_to_key

from interpreter.block import Block
from functions.define import define
from interpreter.stack import Stack

num = int | float


# BLOCK FUNCTIONS

@define("*", "The block %b is executed %a times:")
def repeat(a: int, b: Block, execute: exec):
    for i in range(a):
        execute(b.code, desc=f"Iteration {i + 1}/{a}")


@define("v", "The block %b is executed on a fresh stack with %a arguments, and the results are pushed:")
def scope(a: int, b: Block, execute: exec, s: Stack):
    args = s.top(a)
    res = execute(b.code, Stack(args, parent=s))
    return tuple(res)


@define("?", "The block %b is executed if %a is truthy:")
def if_(a: any, b: Block, execute: exec):
    if a:
        execute(b.code)


@define("/", "The block %b is executed on each element of %a and the previous result. The final result is pushed:")
def reduce(al: list, b: Block, execute: exec, s: Stack):
    last = al[0]
    for a in al[1:]:
        args = [last, a]
        last = execute(b.code, Stack(args, parent=s))[0]
    return last


@define("/", "The block %b is executed on each element of %a and the previous result, starting with %c."
             "The final result is pushed:")
def reduce(al: list, b: Block, c: any, execute: exec, s: Stack):
    last = c
    for a in al:
        args = [last, a]
        last = execute(b.code, Stack(args, parent=s))[0]
    return last


@define("\\", "The block %b is executed one each element of %a and the previous result. The results list is pushed:")
def scan(al: list, b: Block, execute: exec, s: Stack):
    out = [al[0]]
    for a in al[1:]:
        args = [out[-1], a]
        res = execute(b.code, Stack(args, parent=s))
        out.append(res[-1])
    return tuple(out)


@define("w", "The block %a is executed while the element on the top of the stack is truthy:")
def while_(a: Block, execute: exec, s: Stack):
    while len(s) > 0 and s[-1]:
        execute(a.code)


@define("m", "The block %b is mapped over the elements of %a:", vectorize=False)
def map_(al: list, b: Block, execute: exec, s: Stack):
    return [execute(b.code, Stack([a], parent=s))[-1] for a in al]


@define("M", "The block %b is mapped over the elements of %a, with %c additional items from the stack in scope:",
        vectorize=False)
def map_with_args(al: list, b: Block, c: int, execute: exec, s: Stack):
    args = s.pop_n(c)
    return [execute(b.code, Stack([*args, a], parent=s))[-1] for a in al]


@define("p", "The block %b is mapped over each consecutive pair of %a", vectorize=False)
def pairwise_map(al: list, b: Block, execute: exec, s: Stack):
    return [execute(b.code, Stack([a1, a2], parent=s))[-1] for a1, a2 in itertools.pairwise(al)]


# COMPARISON

@define("=", "1 is pushed if %a == %b, else 0 is pushed.")
def equals(a: any, b: any) -> int:
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


@define("j", "The elements of %a are concatenated.")
def join(al: list) -> str:
    return "".join(map(str, al))


@define("o", "%a is decoded into ascii code point(s).")
def ordinal(a: str) -> int | list[int]:
    return ord(a) if len(a) == 1 else [ord(c) for c in a]


@define("F", "%a is split on whitespace.")
def fields(a: str) -> list[str]:
    return re.split(r"\s+", a)


@define("p", "%a is padded on both sides with spaces to be %b chars long.")
def pad(a: str, b: int) -> str:
    return a.center(b, " ")


@define("*", "%a is repeated %b times.")
def pad(a: str, b: int) -> str:
    return a * b


@define("`m", "A list of matches of the regex %b found in %a is pushed")
def regex_matches(a: str, b: str) -> list:
    return re.findall(b, a)


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


@define("u", "Each item of %a is pushed.", vectorize=False)
def unwrap(a: list) -> tuple:
    return tuple(a)


@define("_", "A list of each scalar nested in %a is pushed.", vectorize=False)
def flatten(a: list) -> list:
    def flatten_once(arr):
        if isinstance(arr, list):
            return sum(map(flatten_once, arr), [])
        return [arr]

    return flatten_once(a)


@define("e", "A list of %a items popped from the stack is pushed.")
def enlist(a: int, s: Stack) -> list:
    return list(reversed([s.pop() for _ in range(a)]))


@define("i", "The %bth item of %a is pushed.")
def index(al: list, b: int) -> any:
    return al[b]


@define("i", "The %bth character of %a is pushed.")
def index(a: str, b: int) -> any:
    return a[b]


@define("i", "A list of elements from %a corresponding to indexes in %b is pushed.", vectorize=False)
def index(al: list, bl: list) -> list:
    return [al[b] for b in bl]


@define("i", "A list of characters from %a corresponding to indexes in %b is pushed.", vectorize=False)
def index(a: str, bl: list) -> list:
    return [a[b] for b in bl]


@define("@", "The index of each item of %b in %a is pushed.")
def index_of(al: list, bl: list) -> any:
    return [al.index(b) if b in al else -1 for b in bl]


@define("@", "The index of %b in %a is pushed.")
def index_of(al: list, b: any) -> any:
    return al.index(b)


@define("@", "The index of the substring %b in %a is pushed.")
def index_of(al: str, b: any) -> any:
    return al.index(str(b))


@define("P", "%a is split into %b-item chunks.", vectorize=False)
def partition(al: list | str, b: num) -> list:
    return [al[i:i + int(b)] for i in range(0, len(al), int(b))]


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


@define("N", "The intersection of %a and %b is pushed.", vectorize=False)
def intersection(al: list | str, bl: list | str) -> list:
    return [a for a in al if a in bl]


@define("-", "The difference of %a and %b is pushed.")
def difference(al: list | str, bl: list | str) -> list:
    return [a for a in al if a not in bl]


@define("-", "All instances of %b are removed from %a.")
def remove(al: list, b: any) -> list:
    return [a for a in al if a != b]


@define("l", "The length of %a is pushed.", vectorize=False)
def length(al: list | str) -> int:
    return len(al)


@define("d", "A list of the unique items in %a are pushed.")
def deduplicate(al: list) -> list:
    return list(set(al))


@define("z", "%a is zipped with %b.", vectorize=False)
def zip_(a: list | str, b: list | str) -> list:
    return [list(x) for x in zip(a, b)]


@define("Z", "All items of %a are zipped together", vectorize=False)
def zip_all(al: list) -> list:
    return [list(x) for x in zip(*al)]


@define("*", "%a is repeated %b times.", vectorize=False)
def repeat(a: list, b: int) -> list:
    return a * b


@define("S", "The sum of all elements of %a is pushed.")
def sum_(al: list) -> any:
    return sum(al)


@define("C", "The length-%b combinations of %a are pushed.")
def combinations(al: list | str, b: int) -> list:
    return list(map(list, itertools.combinations(al, b)))


@define("T", "The transpose of the 2D list %a is pushed.", vectorize=False)
def transpose(al: list) -> list:
    if len(al) == 0:
        return []
    if type(al[0]) is list:
        return [list(z) for z in zip(*al)]
    if type(al[0]) is str:
        return ["".join(z) for z in zip(*al)]
    return al


@define(")", "The list %a is sorted ascending and pushed.", vectorize=False)
def transpose_ascending(al: list) -> list:
    return sorted(al)


@define("(", "The list %a is sorted descending and pushed.", vectorize=False)
def transpose_descending(al: list) -> list:
    return sorted(al, reverse=True)


@define(")", "The list %a is sorted ascending by keys produced by %b and pushed.", vectorize=False)
def transpose_ascending(al: list, b: Block, execute: exec, s: Stack) -> list:
    def cmp(x, y):
        return execute(b.code, Stack([x, y], parent=s))[-1]
    return sorted(al, key=cmp_to_key(cmp))


@define("(", "The list %a is sorted descending by keys produced by %b and pushed.", vectorize=False)
def transpose_descending(al: list, b: Block, execute: exec, s: Stack) -> list:
    def cmp(x, y):
        return execute(b.code, Stack([x, y], parent=s))[-1]
    return sorted(al, reverse=True, key=cmp_to_key(cmp))


@define("g", "Group elements of %a by value", vectorize=False)
def group_by_identity(al: list) -> list:
    groups = {}
    for a in al:
        if a in groups:
            groups[a].append(a)
        else:
            groups[a] = [a]
    return list(groups.values())


@define("g", "Group elements of %a by a key provided by %b", vectorize=False)
def group_by(al: list, b: Block, execute: exec, s: Stack) -> list:
    pairs = [(execute(b.code, Stack([a], parent=s))[-1], a) for a in al]
    groups = {}
    for k, v in pairs:
        if k in groups:
            groups[k].append(v)
        else:
            groups[k] = [v]
    return list(groups.values())


@define("$", "Count occurrences of %b in %a", vectorize=False)
def count(al: list, b: any) -> int:
    return al.count(b)


@define("_", "The item of %a at index %b is removed", vectorize=False)
def drop_index(al: list, b: int) -> list:
    return al[:b] + al[b + 1:]


@define("w", "A list of windows of size %b in list %a is pushed", vectorize=False)
def windows(al: list | str, b: int) -> list:
    return [al[i:i + b] for i in range(len(al) - b + 1)]


@define(">", "The first %b elements of %a are dropped")
def start(al: list | str, n: int) -> list:
    return al[n:]


@define("<", "The last %b elements of %a are dropped")
def end(al: list | str, n: int) -> list:
    return al[:n]


@define("R", "The reverse of %a is pushed", vectorize=False)
def end(al: list) -> list:
    return list(reversed(al))


@define("R", "The reverse of %a is pushed", vectorize=False)
def end(al: str) -> str:
    return "".join(reversed(al))


@define("h", "1 is pushed if %a has member %b", vectorize=False)
def has(al: list, b: any) -> int:
    if type(b) in [str, int, float]:
        return int(b in al)
    return int(any(a == b for a in al))


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


@define("A", "The string of alphanumeric ascii characters is pushed.")
def alphanumeric() -> str:
    return "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


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


@define("#", "The %ta %a is discarded.", vectorize=False)
def void(_: any):
    pass


@define("`v", "The top element from the parent stack is pushed")
def borrow(s: Stack):
    return s.parent[-1]


# INPUT / OUTPUT

@define(".", "The %ta %a is printed to the console.", vectorize=False)
def print_(a: any):
    print(a)


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


@define("¦", "The absolute value of %a is pushed")
def magnitude(a: num) -> num:
    return abs(a)


@define("~", "The sign of %a is pushed")
def sign(a: num) -> int:
    if a > 0:
        return 1
    if a < 0:
        return -1
    return 0


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
