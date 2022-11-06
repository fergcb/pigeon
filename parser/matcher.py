from dataclasses import dataclass
import re
from typing import Any


@dataclass
class Result:
    value: Any
    text: str


Empty = Result(None, "")
Fail = Result(None, "FAIL")


class Matcher:
    def __call__(self, source) -> (Result, str):
        return Fail

    def __rshift__(self, action):
        return Process(self, action)

    def __add__(self, other):
        return Sequence(self, other)

    def __or__(self, other):
        return Alternate(self, other)


class Optional(Matcher):
    def __init__(self, matcher):
        self.matcher = matcher

    def __call__(self, source) -> (Result, str):
        match, rest = self.matcher(source)
        if match is not Fail:
            return Result(match.value, match.text), rest
        return Empty, source


class Sequence(Matcher):
    def __init__(self, *matchers, ignore_whitespace=True):
        self.matchers = matchers
        self.ignore_whitespace = ignore_whitespace

    def __add__(self, matcher):
        return Sequence(*self.matchers, matcher)

    def __call__(self, source) -> (Result, str):
        matches = []
        text = ""
        rest = source
        for matcher in self.matchers:
            if self.ignore_whitespace:
                ws = rest[:-len(rest.lstrip())]
                text += ws
                rest = rest.lstrip()
            match, rest = matcher(rest)
            if match is Fail:
                return Fail, source
            matches.append(match.value)
            text += match.text
        if self.ignore_whitespace:
            rest = rest.lstrip()
        return Result(matches, text), rest


class Alternate(Matcher):
    def __init__(self, *matchers):
        self.matchers = matchers

    def __or__(self, matcher):
        return Alternate(*self.matchers, matcher)

    def __call__(self, source) -> (Result, str):
        for matcher in self.matchers:
            match, rest = matcher(source)
            if match is not Fail:
                return Result(match.value, match.text), rest
        return Fail, source


class Repeat(Matcher):
    def __init__(self, matcher, ignore_whitespace=True):
        self.matcher = matcher
        self.ignore_whitespace = ignore_whitespace

    def __call__(self, source) -> (Result, str):
        matches = []
        text = ""
        rest = source
        while len(rest) > 0:
            if self.ignore_whitespace:
                ws = rest[:-len(rest.lstrip())]
                text += ws
                rest = rest.lstrip()
            match, rest = self.matcher(rest)
            if match is Fail:
                break
            matches.append(match.value)
            text += match.text
        if self.ignore_whitespace:
            ws = rest[:-len(rest.lstrip())]
            text += ws
            rest = rest.lstrip()
        if len(matches) > 0:
            return Result(matches, text), rest
        return Fail, source


class Symbol(Matcher):
    def __init__(self, value):
        self.value = value

    def __call__(self, source) -> (Result, str):
        if source.startswith(self.value):
            match = self.value
            rest = source[len(match):]
            return Result(match, match), rest
        return Fail, source


class RegExp(Matcher):
    def __init__(self, expr):
        self.expr = expr

    def __call__(self, source) -> (Result, str):
        re_match = re.match(self.expr, source)
        if re_match is not None:
            match = re_match.group(0)
            rest = source[len(match):]
            return Result(match, match), rest
        return Fail, source


class Lazy(Matcher):
    def __init__(self, matcher_func):
        self.matcher_func = matcher_func
        self.matcher = None

    def __call__(self, source) -> (Result, str):
        if self.matcher is None:
            self.matcher = self.matcher_func()
        return self.matcher(source)


class Process(Matcher):
    def __init__(self, matcher, action):
        self.matcher = matcher
        self.action = action

    def __call__(self, source) -> (Result, str):
        match, rest = self.matcher(source)
        if match is Fail:
            return Fail, source
        processed = self.action(match)

        return Result(processed, match.text), rest


class EOF(Matcher):
    def __call__(self, source) -> (Result, str):
        if len(source) == 0:
            return Empty, source
        return Fail, source
