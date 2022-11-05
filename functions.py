import copy
from dataclasses import dataclass
from typing import Callable, Any, Optional

# A signature is a set of argument types and the corresponding action
Signature = tuple[tuple[type, ...], Callable, str]


@dataclass
class Function:
    """
    The set of possible stack operations a symbol can represent (signatures)
    """
    symbol: str
    sigs: list[Signature]
    allow_arrays: bool


# The set of defined functions
_functions: dict[str, Function] = {}


def define(symbol: str, sigs: list[Signature], allow_arrays: bool = True):
    """
    Define a new function
    """
    if symbol in _functions:
        raise Exception(f"The symbol {symbol} is already bound to a function.")
    _functions[symbol] = Function(symbol, sigs, allow_arrays)


def get_all() -> list[Function]:
    return copy.deepcopy(list(_functions.values()))


def get_func(symbol: str) -> Function:
    """
    Get a function from the set by its symbol
    """
    return _functions[symbol]


def is_list_of(v: Any, t: type) -> bool:
    """
    Check whether a value is a list of a given type
    """
    return type(v) is list and (len(v) == 0 or t is ... or type(v[0]) is t)


def match_func(symbol: str, stack: list) -> Optional[tuple[Signature, bool]]:
    """
    Check whether the stack is applicable to any signature of the given function,
    returning the matching signature, if any
    """
    func = get_func(symbol)
    for sig in func.sigs:
        arg_types, action, _ = sig
        if match_args(arg_types, stack, func.allow_arrays):
            return sig, func.allow_arrays
    return None


def match_args(arg_types: tuple, stack: list, allow_arrays: bool) -> bool:
    """
    Check whether a signature's parameter types match
    the types of the values at the top of the stack
    """
    # If the function takes no args, always match
    if arg_types == ():
        return True

    # If there aren't enough items on the stack, never match
    if len(stack) < len(arg_types):
        return False

    top = stack[-len(arg_types):]

    for i, arg_type in enumerate(arg_types):
        # Always match "any" type
        if arg_type is ...:
            continue
        val = top[i]
        # If there isn't a perfect match
        if type(val) is not arg_type:
            # Allow the first argument to be a list of the given type, for array operations
            if allow_arrays and i == 0 and is_list_of(val, arg_type):
                continue
            # Otherwise don't match
            return False

    # If no conflicts are found, it's a match
    return True


# + : ADD
define("+", [
    ((list, list), lambda A, B, s: [a + b for a, b in zip(A, B)],
        "The element-wise sum of %a and %b is pushed."),
    ((int, int), lambda a, b, s: a + b,
        "%a + %b = %res is pushed."),
    ((str, ...), lambda a, b, s: a + str(b),
        "%a and %b are appended as strings."),
    ((..., str), lambda a, b, s: str(a) + b,
        "%a and %b are appended as strings."),
])

# * : MULTIPLY
define("*", [
    ((int, int), lambda a, b, s: a * b,
        "%a × %b = %res is pushed."),
])

# - : SUBTRACT, FILTER
define("-", [
    ((list, list), lambda A, B, s: [a for a in A if a not in B],
        "The difference of %a and %b is pushed."),
    ((list, ...), lambda A, b, s: [a for a in A if a is not b],
        "%b is removed from %a."),
    ((str, str), lambda a, b, s: a.replace(b, ""),
        "%b is removed from %a."),
    ((int, int), lambda a, b, s: a - b,
        "%a - %b = %res is pushed."),
])

# / : DIVIDE
define("/", [
    ((int, int), lambda a, b, s: a / b,
        "%a ÷ %b = %res is pushed."),
])

# % : MODULO
define("%", [
    ((int, int), lambda a, b, s: a % b,
        "%a MOD %b = %res is pushed.")
])

# & : AND
define("&", [
    ((list, list), lambda A, B, s: [a and b for a, b in zip(A, B)],
        "The element-wise AND of %a and %b is pushed."),
    ((..., ...), lambda a, b, s: a and b,
        "The short-circuiting AND of %a and %b is pushed.")
])

# | : OR
define("|", [
    ((list, list), lambda A, B, s: [a or b for a, b in zip(A, B)],
        "The element-wise OR of %a and %b is pushed."),
    ((..., ...), lambda a, b, s: a or b,
        "The short-circuiting OR of %a and %b is pushed.")
])

# j : JOIN
define("j", [
    ((list, str), lambda A, b, s: b.join(map(str, A)),
        "The elements of %a are joined on %b.")
])

# `l : LIST
define("`l", [
    ((str,), lambda a, s: list(a),
        "%a is cast to a list.")
])

# `s : STRING
define("`s", [
    ((...,), lambda a, s: str(a),
        "%a is cast to a string.")
])

# `n : NUM, cast to INT
define("`n", [
    ((str,), lambda a, s: int(a),
        "%a is cast to an integer.")
])

# `f : FLOAT, cast to float
define("`f", [
    ((str,), lambda a, s: float(a),
        "%a is cast to a float, and pushed."),
    ((int,), lambda a, s: float(a),
        "%a is cast to a float, and pushed."),
])

# ^ : RANGE
define("^", [
    ((int,), lambda a, s: list(range(a)),
        "A list of integers from 0 to %a is pushed.")
])

# u : UNWRAP
define("u", [
    ((list,), lambda a, s: tuple(a),
        "Each item of %a is pushed.")
])

# e : ENLIST
define("e", [
    ((int,), lambda a, s: list(reversed([s.pop() for i in range(a)])),
        "A list of %a items popped from the stack is pushed.")
])

# i : INDEX
define("i", [
    ((list, int), lambda A, b, s: A[b],
        "The %bth item of %a is pushed."),
    ((list, list), lambda A, B, s: [A[b] for b in B],
        "A list of elements from %a corresponding to indexes in %b is pushed.")
])

# p : PARTITION
define("p", [
    ((list, int), lambda A, b, s: [A[i:i + b] for i in range(0, len(A), b)],
        "%a is split into %b-item chunks."),
])

# b : BITS
define("b", [
    ((), lambda s: [0, 1],
        "The list [0, 1] is pushed.")
])

# t : TRUTHY
define("t", [
    ((...,), lambda a, s: int(not not a),
        "1 is pushed if the %ta %a is truthy, else 0 is pushed.")
])

# f : FALSY
define("f", [
    ((...,), lambda a, s: int(not a),
        "1 is pushed if the %ta %a is falsy, else 0 is pushed.")
])

# : : DUPLICATE
define(":", [
    ((...,), lambda a, s: ((a, a) if type(a) is not list else (a[:], a[:])),
        "A copy of the %ta %a is pushed.")
], allow_arrays=False)

# `: : DUPLICATE TWO
define("`:", [
    ((..., ...), lambda a, b, s: (a, b, a, b),
        "A copy each of the %ta %a and the %tb %b are pushed.")
], allow_arrays=False)

# c : CYCLE - SWAP top two elements
define("c", [
    ((..., ...), lambda a, b, s: (b, a),
        "The %ta %a and the %tb %b are swapped.")
], allow_arrays=False)

# r : ROTATE
define("r", [
    ((...,), lambda a, s: s.insert(0, a),
        "The %ta %a is moved to the bottom of the stack")
], allow_arrays=False)

# . : OUTPUT
define(".", [
    ((...,), lambda a, s: print(a),
        "The %ta %a is printed to the console."),
], allow_arrays=False)

# , : INPUT
define(",", [
    ((), lambda s: input(),
        "The input %ret %res is pushed.")
])

# ; : INPUT INT
define(";", [
    ((), lambda s: int(input()),
        "The input int %res is pushed.")
])

# `d : DUMP : print the entire stack as a list
define("`d", [
    ((), lambda s: print(s),
        "The contents of the stack is printed.")
])
