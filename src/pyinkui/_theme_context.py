from __future__ import annotations

from typing import Any, cast

from pyinkcli.component import createElement
from pyinkcli.packages.react import createContext, useContext

_themeContext = createContext({})


def getThemeContext() -> dict[str, Any] | None:
    context_value = useContext(_themeContext)
    if isinstance(context_value, dict):
        return context_value
    return None


def provideThemeContext(*children: Any, theme: dict[str, Any]) -> Any:
    return createElement(cast(Any, _themeContext.Provider), *children, value=theme)
