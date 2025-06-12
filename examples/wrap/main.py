from typing import override

import pygoerrors


class SpecialError(pygoerrors.Error):
    def __init__(self, some_prop: int):
        self.__some_prop = some_prop

    @override
    def error(self) -> str:
        return f"special(some_prop={self.__some_prop})"


def work() -> pygoerrors.Result[int]:
    return 0, SpecialError(1)


def work2() -> pygoerrors.Result[int]:
    _, err = work()
    return 0, pygoerrors.errorf("err: %w", err)


if __name__ == "__main__":
    _, err = work2()

    assert err
    assert err.error() == "err: special(some_prop=1)"

    # Since errWork is wrapped in work2 it still is an errWork
    assert pygoerrors.is_(err, SpecialError(1))

    specialErr = pygoerrors.as_(err, SpecialError)
    assert specialErr.error() == "special(some_prop=1)"
