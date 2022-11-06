import string
from typing import Callable, Any


def _is_list_of(v: Any, t: type) -> bool:
    """
    Check whether a value is a list of a given type
    """
    return type(v) is list and (len(v) == 0 or t is any or all(type(x) is t for x in v))


class Function:
    name: str
    symbol: str
    params: tuple[type]
    action: Callable
    can_vectorize: bool
    takes_stack: bool
    desc: str

    def __init__(self, name: str, symbol: str, params: tuple[type], action: Callable, can_vectorize: bool, takes_stack: bool, desc: str):
        self.name = name
        self.symbol = symbol
        self.params = params
        self.action = action
        self.can_vectorize = can_vectorize
        self.takes_stack = takes_stack
        self.desc = desc

    def call(self, stack: list) -> tuple[list, Any, bool]:
        args = []
        for _ in self.params:
            args.insert(0, stack.pop())

        if self.takes_stack:
            args.append(stack)

        # Try a vector operation
        if self.can_vectorize and len(args) > 0 and _is_list_of(args[0], self.params[0]):
            # Apply the action to each item in the list
            return args, list(map(lambda x: self.action(x, *args[1:]), args[0])), True
        # Otherwise scalar
        else:
            return args, self.action(*args), False

    def describe(self, args: Any, res: Any, vectorized: bool = False) -> str:
        desc = self.desc

        if vectorized:
            desc = desc.replace("%a", "N").replace("%ta", "value").replace(".", ",")\
                       + f" where N is each element in %a."

        for i, arg in enumerate(args):
            a = string.ascii_lowercase[i]
            desc = desc.replace(f"%t{a}", type(arg).__name__)
            desc = desc.replace(f"%{a}", repr(arg))

        desc = desc.replace(f"%ret", type(res).__name__)
        desc = desc.replace(f"%res", repr(res))

        return desc

    def match_params(self, stack: list) -> bool:
        # If the function takes no args, always match
        if self.params == ():
            return True

        # If there aren't enough items on the stack, never match
        if len(stack) < len(self.params):
            return False

        top = stack[-len(self.params):]

        for i, param in enumerate(self.params):
            # Always match "any" type
            if param is any:
                continue
            val = top[i]
            # If there isn't a perfect match
            if type(val) is not param:
                # Allow the first argument to be a list of the given type, for array operations
                if self.can_vectorize and i == 0 and _is_list_of(val, param):
                    continue
                # Otherwise don't match
                return False

        # If no conflicts are found, it's a match
        return True
