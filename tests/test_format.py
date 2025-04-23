from typing import override

import pygoerrors


def test_wrap_format():
    err1 = pygoerrors.new("err1")
    err2 = pygoerrors.errorf("err2: %w", err1)

    assert err2.error() == "err2: err1"


def test_nonwrap_format():
    err = pygoerrors.errorf("err: %s", "error")

    assert err.error() == "err: error"


def test_wrap_format_as():
    class SpecialError(pygoerrors.Error):
        def __init__(self, some_prop: int):
            self.__some_prop = some_prop

        @override
        def error(self) -> str:
            return f"special(some_prop={self.__some_prop})"

    def work() -> tuple[int, pygoerrors.Error]:
        return 0, SpecialError(1)

    def work2() -> tuple[int, pygoerrors.Error]:
        _, err = work()
        return 0, pygoerrors.errorf("err: %w", err)

    _, err = work2()
    assert err
    assert err.error() == "err: special(some_prop=1)"

    assert pygoerrors.is_(err, SpecialError(1))

    specialErr = pygoerrors.as_(err, SpecialError)
    assert specialErr
    assert specialErr.error() == "special(some_prop=1)"
