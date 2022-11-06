import functions.definitions
from functions.function_registry import FunctionRegistry as registry

if __name__ == "__main__":
    for g in registry._groups.values():
        for f in g._functions:
            print(f.symbol, f.name, f.params)
