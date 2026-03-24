import json
from typing import Any


def serialize_json(data: dict[str, Any]) -> bytes:
    return json.dumps(data, default=str).encode("utf-8")
