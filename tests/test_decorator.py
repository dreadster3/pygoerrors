from collections.abc import Iterable

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
