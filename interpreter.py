import copy

import functions
from parser.token import Token


def execute(symbol: str, stack: list) -> str:
    """
    Find a function signature corresponding to the given symbol
    and stack state, and execute its action on the stack.

    Returns a string describing what the function did.
    """
    match = functions.match_func(symbol, stack)

    if match is None:
        raise Exception("No matching signature for call to '{}'.".format(symbol))

    func, allow_arrays = match
    arg_types, action, desc = func

    args = [] if arg_types == () else list(reversed([stack.pop() for x in arg_types]))
    # Try an array operation
    if allow_arrays and len(args) > 0 and functions.is_list_of(args[0], arg_types[0]):
        # Apply the action to each item in the list
        ret = list(map(lambda x: action(x, *args[1:], stack), args[0]))
    # Otherwise scalar
    else:
        ret = action(*args, stack)

    # If the action returned something, push it to the stack
    if ret is not None:
        # A tuple means multiple items to push
        if type(ret) is tuple:
            stack.extend(ret)
        else:
            stack.append(ret)

    return desc


def interpret(tokens: list[(Token, any)], explain: bool, stack=None, depth=0) -> list:
    """
    Execute a sequence of tokens on an empty stack,
    and return the resulting stack
    """
    stack = [] if stack is None else stack

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
                    args = stack[-n:]
                    if explain:
                        print(indent + f"({{) The program descends into a new scoped block with {n} arguments.")
                        print(indent + f"     => {args}\n")
                    ret = interpret(ts, explain, stack=copy.deepcopy(args), depth=depth+1)
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
