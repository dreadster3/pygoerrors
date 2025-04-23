import pygoerrors


def work() -> tuple[int, pygoerrors.Error]:
    return 0, pygoerrors.new("err")


if __name__ == "__main__":
    _, err = work()

    assert err
    assert err.error() == "err"
