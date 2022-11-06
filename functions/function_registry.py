from functions.function import Function
from functions.function_group import FunctionGroup


class FunctionRegistry:
    _groups: dict[str, FunctionGroup] = {}

    @staticmethod
    def all() -> list[FunctionGroup]:
        return list(FunctionRegistry._groups.values())

    @staticmethod
    def has(symbol: str) -> bool:
        return symbol in FunctionRegistry._groups

    @staticmethod
    def get(symbol: str) -> FunctionGroup:
        assert FunctionRegistry.has(symbol), f"No such function symbol '{symbol}'."
        return FunctionRegistry._groups[symbol]

    @staticmethod
    def find(symbol: str, stack: list) -> Function:
        if not FunctionRegistry.has(symbol):
            raise Exception(f"No functions are defined for the symbol '{symbol}'.")

        group = FunctionRegistry.get(symbol)
        return group.find_func(stack)

    @staticmethod
    def register(func: Function):
        if not FunctionRegistry.has(func.symbol):
            FunctionRegistry._groups[func.symbol] = FunctionGroup(func.symbol)

        group = FunctionRegistry.get(func.symbol)
        group.register(func)
