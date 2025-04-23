from __future__ import annotations

from typing import override

from pygoerrors.helpers import NotSet, NotSetType
from pygoerrors.protocols import Error, Unwrappable


def new(message: str) -> Error:
    return stringError(message)


def _is(err: Error, target: Error) -> bool:
    while True:
        if err == target:
            return True

        if isinstance(err, Unwrappable):
            err = err.unwrap()
            if not err:
                return False
        else:
            return False


def is_(err: Error, target: Error) -> bool:
    if err or target:
        return err == target

    return _is(err, target)


def as_[T: Error](err: Error, target: type[T]) -> T | NotSetType:
    if not err:
        return NotSet

    while True:
        if isinstance(err, target):
            return err

        if isinstance(err, Unwrappable):
            err = err.unwrap()
            if not err:
                return NotSet
        else:
            return NotSet


class stringError(Error):
    def __init__(self, error: str):
        self.__error = error

    @override
    def error(self) -> str:
        return self.__error
