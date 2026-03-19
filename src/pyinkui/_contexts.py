from __future__ import annotations

from contextlib import contextmanager
from contextvars import ContextVar
from typing import Any, Generator

orderedListContext: ContextVar[dict[str, Any]] = ContextVar('ordered_list_context', default={'marker': ''})
orderedListItemContext: ContextVar[dict[str, Any]] = ContextVar('ordered_list_item_context', default={'marker': '─'})
unorderedListContext: ContextVar[dict[str, Any]] = ContextVar('unordered_list_context', default={'depth': 0})
unorderedListItemContext: ContextVar[dict[str, Any]] = ContextVar('unordered_list_item_context', default={'marker': '─'})


def getOrderedListContext() -> dict[str, Any]:
    return orderedListContext.get()


def getOrderedListItemContext() -> dict[str, Any]:
    return orderedListItemContext.get()


def getUnorderedListContext() -> dict[str, Any]:
    return unorderedListContext.get()


def getUnorderedListItemContext() -> dict[str, Any]:
    return unorderedListItemContext.get()


@contextmanager
def provideOrderedListContext(value: dict[str, Any]) -> Generator[None, None, None]:
    token = orderedListContext.set(value)
    try:
        yield
    finally:
        orderedListContext.reset(token)


@contextmanager
def provideOrderedListItemContext(value: dict[str, Any]) -> Generator[None, None, None]:
    token = orderedListItemContext.set(value)
    try:
        yield
    finally:
        orderedListItemContext.reset(token)


@contextmanager
def provideUnorderedListContext(value: dict[str, Any]) -> Generator[None, None, None]:
    token = unorderedListContext.set(value)
    try:
        yield
    finally:
        unorderedListContext.reset(token)


@contextmanager
def provideUnorderedListItemContext(value: dict[str, Any]) -> Generator[None, None, None]:
    token = unorderedListItemContext.set(value)
    try:
        yield
    finally:
        unorderedListItemContext.reset(token)
