import inspect

import fastapix


def test_smoke() -> None:
    assert inspect.ismodule(fastapix)
