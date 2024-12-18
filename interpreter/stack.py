from typing import Self


class Stack(list):
    def __init__(self, items: list = None, parent: Self = None):
        super().__init__(items or [])
        self.parent = parent

    def top(self, n: int = 1) -> list:
        if n == 0:
            return []
        items = self[-n:]
        return items

    def pop_n(self, n: int) -> list:
        if n == 0:
            return []
        items = self.top(n)
        del self[-n:]
        return items
