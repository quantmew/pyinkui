from __future__ import annotations

from typing import cast

from pyinkcli.packages.react import createContext, useContext

orderedListContext = createContext({'marker': ''})
orderedListItemContext = createContext({'marker': '─'})
unorderedListContext = createContext({'depth': 0})
unorderedListItemContext = createContext({'marker': '─'})


def getOrderedListContext() -> dict[str, str]:
    return cast(dict[str, str], useContext(orderedListContext))


def getOrderedListItemContext() -> dict[str, str]:
    return cast(dict[str, str], useContext(orderedListItemContext))


def getUnorderedListContext() -> dict[str, int]:
    return cast(dict[str, int], useContext(unorderedListContext))


def getUnorderedListItemContext() -> dict[str, str]:
    return cast(dict[str, str], useContext(unorderedListItemContext))
