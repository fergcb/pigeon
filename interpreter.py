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


def interpret(tokens: list[(Token, any)], explain: bool) -> list:
    """
    Execute a sequence of tokens on an empty stack,
    and return the resulting stack
    """
    stack = []

    for token in tokens:
        match token:
            case (Token.LITERAL, x):
                stack.append(x)
                if explain:
                    print(f"\nThe value {repr(x)} is pushed to the stack.")
            case (Token.FUNCTION, f):
                desc = execute(f, stack)
                if explain:
                    print(f"\n({f}) {desc}")
            case _:
                raise Exception(f"Invalid token {token}")
        if explain:
            print(" =>", stack)

    return stack
