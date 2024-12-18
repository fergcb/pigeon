from functions import registry
from parser.tokens import Token, TokenType
from interpreter.stack import Stack


def execute(symbol: str, stack: Stack, explain: bool, depth: int):
    """
    Find a function signature corresponding to the given symbol
    and stack state, and execute its action on the stack.

    Returns a string describing what the function did.
    """
    indent = "    " * depth

    func = registry.find(symbol, stack)

    def executor(code, new_stack=None, desc=None):
        new_stack = stack if new_stack is None else new_stack

        if explain:
            if desc is not None:
                print(desc)
            print(indent + f" => {new_stack}\n")

        return interpret(code, explain, new_stack, depth + 1)

    # Get all the prerequisites for the function call
    args, vectorized, desc = func.prime(stack, executor)

    if explain:
        print(indent + f"{func.name} ({func.symbol}): {desc}")

    # Execute the stack operation
    res = func.call(args, vectorized)

    # If the function returned something, push it to the stack
    if res is not None:
        # A tuple means multiple items to push
        if type(res) is tuple:
            stack.extend(res)
        else:
            stack.append(res)


def interpret(tokens: list[(Token, any)], explain: bool, stack: Stack = None, depth=0) -> Stack:
    """
    Execute a sequence of tokens on an empty stack,
    and return the resulting stack
    """
    stack = Stack() if stack is None else stack

    indent = "    " * depth

    for token in tokens:
        match token:
            case Token(TokenType.LITERAL, x):
                stack.append(x)
                if explain:
                    print(indent + f"The value {repr(x)} is pushed to the stack.")
            case Token(TokenType.FUNCTION, f):
                execute(f, stack, explain, depth)
            case Token(TokenType.COMMENT, _):
                pass
            case _:
                raise Exception(f"Invalid token {token}")
        if explain and token.type is not TokenType.COMMENT:
            print(indent + f" => {stack}\n")

    if depth == 0 and len(stack) > 0:
        print(stack[-1])

    return stack
