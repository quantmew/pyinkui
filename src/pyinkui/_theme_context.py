from __future__ import annotations

from contextlib import contextmanager
from contextvars import ContextVar
from typing import Any, Generator

_themeContext: ContextVar[dict[str, Any] | None] = ContextVar('pyinkui_theme', default=None)


def getThemeContext() -> dict[str, Any] | None:
    return _themeContext.get()


@contextmanager
def provideThemeContext(theme: dict[str, Any]) -> Generator[None, None, None]:
    token = _themeContext.set(theme)
    try:
        yield
    finally:
        _themeContext.reset(token)
