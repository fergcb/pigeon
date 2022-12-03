import string
from types import UnionType
from typing import Callable, Any, get_origin, get_args

from interpreter.stack import Stack


def _is_list_of(v: Any, t: type) -> bool:
    """
    Check whether a value is a list of a given type
    """
    return type(v) is list and (len(v) == 0 or t is any or all(_is_type(x, t) for x in v))


def _is_type(v: Any, t: type) -> bool:
    if get_origin(t) is UnionType:
        return type(v) in get_args(t)
    return type(v) is t


class Function:
    name: str
    symbol: str
    params: tuple[type]
    action: Callable
    can_vectorize: bool
    takes_stack: bool
    takes_executor: bool
    desc: str

    def __init__(self, name: str, symbol: str, params: tuple[type], action: Callable,
                 can_vectorize: bool, takes_stack: bool, takes_executor: bool, desc: str):
        self.name = name
        self.symbol = symbol
        self.params = params
        self.action = action
        self.can_vectorize = can_vectorize
        self.takes_stack = takes_stack
        self.takes_executor = takes_executor
        self.desc = desc

    def prime(self, stack: Stack, executor: Callable):
        args = stack.pop_n(len(self.params))

        if self.takes_executor:
            args.append(executor)

        if self.takes_stack:
            args.append(stack)

        # Check if we can vectorize this operation
        vectorized = self.can_vectorize and len(args) > 0 and _is_list_of(args[0], self.params[0])

        desc = self.describe(args, vectorized)

        return args, vectorized, desc

    def call(self, args: list, vectorized: bool) -> Any:
        if vectorized:
            # Apply the action to each item in the list
            return list(map(lambda x: self.action(x, *args[1:]), args[0]))
        else:
            # Apply the regular, scalar function
            return self.action(*args)

    def describe(self, args: Any, vectorized: bool = False) -> str:
        desc = self.desc

        if vectorized:
            desc = desc.replace("%a", "N").replace("%ta", "value").replace(".", ",")\
                       + f" where N is each element in %a."

        for i, arg in enumerate(args):
            a = string.ascii_lowercase[i]
            desc = desc.replace(f"%t{a}", type(arg).__name__)
            desc = desc.replace(f"%{a}", repr(arg))

        return desc

    def match_params(self, stack: Stack) -> bool:
        param_count = len(self.params)
        # If the function takes no args, always match
        if param_count == 0:
            return True

        # If there aren't enough items on the stack, never match
        if len(stack) < param_count:
            return False

        top = stack.top(param_count)

        for i, param in enumerate(self.params):
            # Always match "any" type
            if param is any:
                continue
            val = top[i]

            # The type is an exact match
            if _is_type(val, param):
                continue

            # No match? Try for vectorization
            if type(val) is not param:
                # Allow the first argument to be a list of the given type, for array operations
                if self.can_vectorize and i == 0 and _is_list_of(val, param):
                    continue
                # Otherwise don't match
                return False

        # If no conflicts are found, it's a match
        return True
