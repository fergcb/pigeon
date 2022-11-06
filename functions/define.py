from typing import Callable, cast, get_type_hints

from functions.function import Function
from functions.function_registry import FunctionRegistry
from stack import Stack


def define(symbol: str, desc: str, *, name: str = None, vectorize: bool = True):
    def decorator(action: Callable):
        nonlocal name, symbol, vectorize
        name = name if name is not None else action.__name__.upper().strip("_")
        hints = get_type_hints(action)
        if "return" in hints:
            hints.pop("return")
        params = cast(tuple[type], tuple(hints.values()))
        if len(params) > 0 and params[-1] is Stack:
            params = params[:-1]
            takes_stack = True
        else:
            takes_stack = False
        func = Function(name, symbol, params, action, vectorize, takes_stack, desc)
        FunctionRegistry.register(func)

        def no_call():
            raise Exception("Do not call Pigeon stack functions directly.")

        return no_call

    return decorator
