# -*- coding: utf-8 -*-
import json

from dataclasses import dataclass

from .serialization import dumps


def test_dumps():
    @dataclass
    class Dummy:
        value: int

    data = Dummy(1)
    expected = {"value": 1}
    observed = dumps(data)
    assert json.loads(observed) == expected
