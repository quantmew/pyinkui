from __future__ import annotations


def _platform_value(unix: str, windows: str | None = None) -> str:
    return unix


pointer = _platform_value('❯')
tick = _platform_value('✔')
cross = _platform_value('✖')
warning = _platform_value('⚠')
info = _platform_value('ℹ')
line = _platform_value('─')
square = _platform_value('█')
squareLightShade = _platform_value('░')
