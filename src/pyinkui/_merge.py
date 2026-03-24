from __future__ import annotations

from copy import deepcopy
from typing import Any


def deepMerge(originalTheme: dict[str, Any], newTheme: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(originalTheme, dict) or not isinstance(newTheme, dict):
        return deepcopy(newTheme)

    merged = deepcopy(originalTheme)
    for key, value in newTheme.items():
        if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
            merged[key] = deepMerge(merged[key], value)
        else:
            merged[key] = deepcopy(value)
    return merged
