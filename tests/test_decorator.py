import time
from collections.abc import Iterable

import cachetools

import pygoerrors


def some_function() -> int:
    raise Exception("some error")


def generator() -> Iterable[int]:
    yield 1
    yield 2
    raise Exception("some error")
    yield 3


def test_decorator():
    wrapped = pygoerrors.to_errors(some_function)

    _, err = wrapped()

    assert err
    assert err.error() == "some error"


def test_iterable_decorator():
    wrapped = pygoerrors.to_errors_iterable(generator)

    iterator = wrapped()
    assert not iterator.err()

    collected = list(iterator)

    assert len(collected) == 2
    assert iterator.err()
    assert iterator.err().error() == "some error"


def test_cache_error_decorator() -> None:
    calls = 0

    @pygoerrors.cache_ok(cache={})
    def other_function(test: int) -> pygoerrors.Result[int]:
        nonlocal calls
        calls += 1
        return test, pygoerrors.new("error")

    _, err = other_function(10)
    _, err = other_function(10)
    _, err = other_function(10)
    _, err = other_function(10)

    assert err
    assert err.error() == "error"
    assert calls == 4


def test_cache_ok_decorator() -> None:
    calls = 0

    @pygoerrors.cache_ok(cache={})
    def other_function(test: int) -> pygoerrors.Result[int]:
        nonlocal calls
        calls += 1
        return test, pygoerrors.Nil

    _, err = other_function(10)
    _, err = other_function(10)
    _, err = other_function(10)
    _, err = other_function(10)

    assert not err
    assert calls == 1


def test_cache_ok_decorator_with_ttl() -> None:
    calls = 0

    @pygoerrors.cache_ok(cache=cachetools.TTLCache(128, 0.1))
    def other_function(test: int) -> pygoerrors.Result[int]:
        nonlocal calls
        calls += 1
        return test, pygoerrors.Nil

    _, err = other_function(10)
    _, err = other_function(10)
    time.sleep(0.1)
    _, err = other_function(10)
    _, err = other_function(10)

    assert not err
    assert calls == 2
