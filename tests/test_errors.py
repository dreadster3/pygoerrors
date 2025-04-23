from typing import override

import pygoerrors
from pygoerrors.helpers import NotSet


def test_error_representation():
    err = pygoerrors.new("test")

    assert repr(err) == "test", err


def test_error_str():
    err = pygoerrors.new("test")

    assert str(err) == "test", err


def test_error_bool():
    err = pygoerrors.new("test")

    assert bool(err)


def test_error_bool_false():
    err = NotSet

    assert not bool(err)


def test_error_is():
    err = pygoerrors.new("test")
    err2 = pygoerrors.new("test")

    assert pygoerrors.is_(err, err2)


def test_error_is_different():
    err = pygoerrors.new("test")
    err2 = pygoerrors.new("test2")

    assert not pygoerrors.is_(err, err2)


def test_error_as():
    class SpecialError(pygoerrors.Error):
        def __init__(self, some_prop: int):
            self.__some_prop = some_prop

        @override
        def error(self) -> str:
            return f"special(some_prop={self.__some_prop})"

    def work() -> tuple[int, pygoerrors.Error]:
        return 0, SpecialError(1)

    _, err = work()
    err2 = pygoerrors.as_(err, SpecialError)

    assert err == err2
    assert type(err2) is SpecialError


def test_error_as_none():
    class SpecialError(pygoerrors.Error):
        def __init__(self, some_prop: int):
            self.__some_prop = some_prop

        @override
        def error(self) -> str:
            return f"special(some_prop={self.__some_prop})"

    def work() -> tuple[int, pygoerrors.Error]:
        return 10, pygoerrors.NotSet

    _, err = work()
    err2 = pygoerrors.as_(err, SpecialError)

    assert err == err2
    assert err2 == NotSet
