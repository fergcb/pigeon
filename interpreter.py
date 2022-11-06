import copy

from functions import registry
from parser.token import Token
from stack import Stack


def execute(symbol: str, stack: Stack) -> str:
    """
    Find a function signature corresponding to the given symbol
    and stack state, and execute its action on the stack.

    Returns a string describing what the function did.
    """
    func = registry.find(symbol, stack)

    # Execute the stack operation
    args, res, vectorized = func.call(stack)

    # If the function returned something, push it to the stack
    if res is not None:
        # A tuple means multiple items to push
        if type(res) is tuple:
            stack.extend(res)
        else:
            stack.append(res)

    return func.describe(args, res, vectorized)


def interpret(tokens: list[(Token, any)], explain: bool, stack: Stack = None, depth=0) -> list:
    """
    Execute a sequence of tokens on an empty stack,
    and return the resulting stack
    """
    stack = Stack() if stack is None else stack

    indent = "    " * depth

    for token in tokens:
        match token:
            case (Token.LITERAL, x):
                stack.append(x)
                if explain:
                    print(indent + f"The value {repr(x)} is pushed to the stack.")
            case (Token.FUNCTION, f):
                desc = execute(f, stack)
                if explain:
                    print(indent + f"({f}) {desc}")
            case (Token.SCOPE, ts):
                if len(stack) > 0 and type(stack[-1]) is int:
                    n = stack.pop()
                    args = stack.top(n)
                    if explain:
                        print(indent + f"({{) The program descends into a new scoped block with {n} arguments.")
                        print(indent + f"     => {args}\n")
                    ret = interpret(ts, explain, stack=Stack(args), depth=depth+1)
                    stack.extend(ret)
                    if explain:
                        print(indent + "(}) The program ascends to the parent scope and the return values are pushed.")
                else:
                    raise Exception("No argument found for scope. Must specify a number of args to copy.")
            case (Token.REPEAT, ts):
                if len(stack) > 0 and type(stack[-1]) is int:
                    n = stack.pop()
                    if explain:
                        print(indent + "(R) The program enters a loop.")
                        print(indent + f" => {stack}\n")
                    for i in range(n):
                        if explain:
                            print(indent + f"Loop iteration {i+1}/{n}:")
                            print(indent + f" => {stack}\n")
                        interpret(ts, explain, stack=stack, depth=depth+1)
                else:
                    raise Exception("No argument found for loop.")

                if explain:
                    print(indent + "(}) The program exits the loop.")

            case _:
                raise Exception(f"Invalid token {token}")
        if explain:
            print(indent + f" => {stack}\n")

    if depth == 0 and len(stack) > 0:
        print(stack[-1])

    return stack
