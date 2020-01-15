# -*- coding: utf-8 -*-
import dataclasses, json

__all__ = (
    "dumps",
)

def dumps(data):
    return json.dumps(data, cls=CustomJSONEncoder)


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)
