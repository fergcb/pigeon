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
    _functions[symbol] = Function(symbol, sigs, allow_arrays)


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
        "Two lists are popped and their element-wise sum is pushed."),
    ((int, int), lambda a, b, s: a + b,
        "Two integers are popped and their sum is pushed."),
    ((str, ...), lambda a, b, s: a + str(b),
        "Two items are popped an appended as strings."),
    ((..., str), lambda a, b, s: str(a) + b,
        "Two items are popped an appended as strings."),
])

# * : MULTIPLY
define("*", [
    ((int, int), lambda a, b, s: a * b,
        "Two integers are popped and their product is pushed."),
])

# - : SUBTRACT, FILTER
define("-", [
    ((list, list), lambda A, B, s: [a for a in A if a not in B],
        "Two lists are popped, and a list containing elements in the second and not in the first is pushed."),
    ((list, ...), lambda A, b, s: [a for a in A if a is not b],
        "An item is popped and all instances of it are removed from a list on the top of the stack."),
    ((str, str), lambda a, b, s: a.replace(b, ""),
        "A string is popped, and all instances of it are removed from the top string."),
    ((int, int), lambda a, b, s: a - b,
        "Two integers are popped, and their difference is pushed."),
])

# % : MODULO
define("%", [
    ((int, int), lambda a, b, s: a % b,
        "Two integers are pushed, and the remainder of integer division is pushed.")
])

# & : AND
define("&", [
    ((list, list), lambda A, B, s: [a and b for a, b in zip(A, B)],
        "Two lists are popped, and their element-wise AND is pushed."),
    ((..., ...), lambda a, b, s: a and b,
        "Two items are popped and their short-circuiting AND is pushed.")
])

# | : OR
define("|", [
    ((list, list), lambda A, B, s: [a or b for a, b in zip(A, B)],
        "Two lists are popped, and their element-wise OR is pushed."),
    ((..., ...), lambda a, b, s: a or b,
        "Two items are popped and their short-circuiting OR is pushed.")
])

# j : JOIN
define("j", [
    ((list, str), lambda A, b, s: b.join(map(str, A)),
        "A string is popped and used to join the elements of the top list.")
])

# l : LIST
define("l", [
    ((...,), lambda a, s: list(a),
        "The top item is cast to a list.")
])

# s : STRING
define("s", [
    ((...,), lambda a, s: str(a),
        "The top item is cast to a string.")
])

# n : NUM, cast to INT
define("n", [
    ((...,), lambda a, s: int(a),
        "The top item is cast to an integer.")
])

# ^ : RANGE
define("^", [
    ((int,), lambda a, s: list(range(a)),
        "An integer is popped, and a list of integers from 0 to that integer is pushed.")
])

# u : UNWRAP
define("u", [
    ((list,), lambda a, s: tuple(a),
        "A list is popped and each of its items are pushed.")
])

# i : INDEX
define("i", [
    ((list, int), lambda A, b, s: A[b],
        "An integer is popped, and the element at that index of a popped list is pushed."),
    ((list, list), lambda A, B, s: [A[b] for b in B],
        "Two lists are popped, and a list of elements from the second corresponding to indexes in the first is pushed.")
])

# b : BITS
define("b", [
    ((), lambda s: [0, 1],
        "A list of the binary digits, 0 and 1, is pushed.")
])

# t : TRUTHY
define("t", [
    ((...,), lambda a, s: int(not not a),
        "1 is pushed if a popped item is truthy, else 0 is pushed.")
])

# f : FALSY
define("f", [
    ((...,), lambda a, s: int(not a),
        "1 is pushed if a popped item is falsy, else 0 is pushed.")
])

# : : DUPLICATE
define(":", [
    ((...,), lambda a, s: ((a, a) if type(a) is not list else (a[:], a[:])),
        "A copy of the item on the top of the stack is pushed.")
], allow_arrays=False)

# `: : DUPLICATE TWO
define("`:", [
    ((..., ...), lambda a, b, s: (a, b, a, b),
        "A copy of the two items on the top of the stack are pushed.")
], allow_arrays=False)

# c : CYCLE - SWAP top two elements
define("c", [
    ((..., ...), lambda a, b, s: (b, a),
        "The two elements on the top of the stack are swapped.")
], allow_arrays=False)

# r : ROTATE
define("r", [
    ((...,), lambda a, s: s.insert(0, a),
        "Pop an item and move it to the bottom of the stack")
], allow_arrays=False)

# . : OUTPUT
define(".", [
    ((...,), lambda a, s: print(a),
        "Pop an item and output it."),
], allow_arrays=False)

# , : INPUT
define(",", [
    ((), lambda s: s.append(input()),
        "Input a string and push it.")
])

# ; : INPUT INT
define(";", [
    ((), lambda s: s.append(int(input())),
        "Input an integer and push it.")
])

# `d : DUMP : print the entire stack as a list
define("`d", [
    ((), lambda s: print(s),
        "Print the entire contents of the stack.")
])
