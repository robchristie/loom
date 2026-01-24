from __future__ import annotations

import json
from hashlib import sha256
from typing import Any


def canonicalize_json(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: canonicalize_json(value[key]) for key in sorted(value)}
    if isinstance(value, list):
        return [canonicalize_json(item) for item in value]
    return value


def canonical_json_bytes(value: Any) -> bytes:
    canonical = canonicalize_json(value)
    return json.dumps(canonical, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha256_canonical_json(value: Any) -> str:
    return sha256(canonical_json_bytes(value)).hexdigest()
