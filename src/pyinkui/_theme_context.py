from __future__ import annotations

from typing import Any

from pyinkcli.component import createElement
from pyinkcli.packages.react import createContext, useContext

_themeContext = createContext(None)


def getThemeContext() -> dict[str, Any] | None:
    return useContext(_themeContext)


def provideThemeContext(*children: Any, theme: dict[str, Any]) -> Any:
    return createElement(_themeContext.Provider, *children, value=theme)
