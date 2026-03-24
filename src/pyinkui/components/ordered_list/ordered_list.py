from __future__ import annotations

from typing import Any, Callable, Protocol, cast

from pyinkcli import Box, Text
from pyinkcli.component import createElement
from pyinkcli.component import isElement
from pyinkui._contexts import getOrderedListContext, getOrderedListItemContext, orderedListContext, orderedListItemContext
from pyinkui.theme import useComponentTheme


class _ListComponent(Protocol):
    Item: Callable[..., Any]

    def __call__(self, *children: Any) -> Any: ...


def _OrderedListItem(*children: Any) -> Any:
    marker = getOrderedListItemContext()['marker']
    styles = useComponentTheme('OrderedList')['styles']
    return Box(Text(marker, **styles['marker']()), Box(*children, **styles['content']()), **styles['listItem']())


def OrderedListItem(*children: Any) -> Any:
    return createElement(_OrderedListItem, *children)


def _OrderedList(*children: Any) -> Any:
    parentMarker = getOrderedListContext()['marker']
    styles = useComponentTheme('OrderedList')['styles']
    numberOfItems = 0
    for child in children:
        if isElement(child) and getattr(child, 'type', None) is _OrderedListItem:
            numberOfItems += 1
    maxMarkerWidth = len(str(numberOfItems))
    wrappedChildren = []
    itemIndex = 0
    for child in children:
        if not (isElement(child) and getattr(child, 'type', None) is _OrderedListItem):
            wrappedChildren.append(child)
            continue
        itemIndex += 1
        paddedMarker = f"{str(itemIndex).rjust(maxMarkerWidth)}."
        marker = f"{parentMarker}{paddedMarker}"
        wrappedChildren.append(
                createElement(
                cast(Any, orderedListContext.Provider),
                createElement(
                    cast(Any, orderedListItemContext.Provider),
                    child,
                    value={'marker': marker},
                ),
                value={'marker': marker},
            )
        )
    return Box(*wrappedChildren, **styles['list']())


def _ordered_list(*children: Any) -> Any:
    return createElement(_OrderedList, *children)


OrderedList = cast(_ListComponent, _ordered_list)
OrderedList.Item = OrderedListItem
