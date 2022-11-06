from functions.function import Function
from typing import Optional


class FunctionGroup:
    """
    The set of possible stack operations a symbol can represent (signatures)
    """
    symbol: str
    functions: list[Function]

    def __init__(self, symbol):
        self.symbol = symbol
        self.functions = []

    def find_func(self, stack: list) -> Optional[Function]:
        for func in self.functions:
            if func.match_params(stack):
                return func
        raise Exception(f"Invalid stack state for function '{self.symbol}'.")

    def register(self, func: Function):
        for existing_func in self.functions:
            if existing_func.params == func.params:
                raise Exception(
                    f"The function '{func.symbol}' {func.name}{repr(func.params)} clashes with {existing_func.name}.")
        self.functions.append(func)
