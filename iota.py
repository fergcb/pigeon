def iota(reset=False):
    """
    Return the next integer in the series of natural numbers,
    starting at 0.

    If reset == True, start again at 0.
    """
    global __iota__
    if reset:
        __iota__ = 0
    current = __iota__
    __iota__ += 1
    return current


__iota__ = 0
