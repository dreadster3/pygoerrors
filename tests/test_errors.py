from typing import override

import pygoerrors


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
    err = pygoerrors.Nil

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
        return 10, pygoerrors.Nil

    _, err = work()
    err2 = pygoerrors.as_(err, SpecialError)

    assert err == err2
    assert err2 == pygoerrors.Nil


def test_error_join():
    err1 = pygoerrors.new("test1")
    err2 = pygoerrors.new("test2")

    actual = pygoerrors.join(err1, err2)
    expected = pygoerrors.new("test1\ntest2")

    assert actual == expected


def test_error_join_some_Nil():
    err1 = pygoerrors.new("test1")
    err2 = pygoerrors.new("test2")
    err3 = pygoerrors.Nil

    actual = pygoerrors.join(err1, err2, err3)
    expected = pygoerrors.new("test1\ntest2")

    assert actual == expected


def test_error_join_all_not_set():
    err1 = pygoerrors.Nil
    err2 = pygoerrors.Nil
    err3 = pygoerrors.Nil

    actual = pygoerrors.join(err1, err2, err3)
    expected = pygoerrors.Nil

    assert actual == expected


def test_error_join_empty():
    actual = pygoerrors.join()
    expected = pygoerrors.Nil

    assert actual == expected
