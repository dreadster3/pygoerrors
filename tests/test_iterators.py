from pygoerrors import iterators


def test_error_iterable_with_error():
    def generator():
        yield 1
        yield 2
        raise ValueError("error")

    iterator = iterators.ErrorIterable(generator())
    collected = list(iterator)

    assert len(collected) == 2
    assert iterator.err().error() == "error"


def test_error_iterable_with_early_error():
    def generator():
        yield 1
        yield 2
        raise ValueError("error")
        yield 3

    iterator = iterators.ErrorIterable(generator())
    collected = list(iterator)

    assert len(collected) == 2
    assert iterator.err().error() == "error"
