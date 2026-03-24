from __future__ import annotations

from pyinkcli.packages.react import createContext, useContext

orderedListContext = createContext({'marker': ''})
orderedListItemContext = createContext({'marker': '─'})
unorderedListContext = createContext({'depth': 0})
unorderedListItemContext = createContext({'marker': '─'})


def getOrderedListContext() -> dict[str, str]:
    return useContext(orderedListContext)


def getOrderedListItemContext() -> dict[str, str]:
    return useContext(orderedListItemContext)


def getUnorderedListContext() -> dict[str, int]:
    return useContext(unorderedListContext)


def getUnorderedListItemContext() -> dict[str, str]:
    return useContext(unorderedListItemContext)
