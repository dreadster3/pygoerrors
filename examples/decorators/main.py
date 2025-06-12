import cachetools

import pygoerrors

calls = 0
calls_error = 0


@pygoerrors.to_errors
def non_error() -> int:
    raise Exception("error")
    return 10


@pygoerrors.cache_ok(cache=cachetools.LRUCache(128))
def some_function() -> pygoerrors.Result[int]:
    global calls
    calls += 1

    return 10, pygoerrors.Nil


@pygoerrors.cache_ok(cache=cachetools.LRUCache(128))
def some_function_error() -> pygoerrors.Result[int]:
    global calls_error
    calls_error += 1

    return 10, pygoerrors.new("some error")


if __name__ == "__main__":
    _, err = non_error()

    assert err
    assert err.error() == "error"

    _, err = some_function()
    _, err = some_function()
    _, err = some_function()
    _, err = some_function()
    _, err = some_function()

    assert not err
    assert calls == 1

    _, err = some_function_error()
    _, err = some_function_error()
    _, err = some_function_error()
    _, err = some_function_error()

    assert err
    assert err.error() == "some error"
    assert calls_error == 4
