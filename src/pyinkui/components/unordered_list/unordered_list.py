from __future__ import annotations

from typing import Any, Callable, Protocol, cast

from pyinkcli import Box, Text
from pyinkcli.component import createElement
from pyinkui._contexts import getUnorderedListContext, getUnorderedListItemContext, unorderedListContext, unorderedListItemContext
from pyinkui._figures import line as defaultMarker
from pyinkui.theme import useComponentTheme


class _ListComponent(Protocol):
    Item: Callable[..., Any]

    def __call__(self, *children: Any) -> Any: ...


def _UnorderedListItem(*children: Any) -> Any:
    marker = getUnorderedListItemContext()['marker']
    styles = useComponentTheme('UnorderedList')['styles']
    return Box(Text(marker, **styles['marker']()), Box(*children, **styles['content']()), **styles['listItem']())


def UnorderedListItem(*children: Any) -> Any:
    return createElement(_UnorderedListItem, *children)


def _UnorderedList(*children: Any) -> Any:
    depth = getUnorderedListContext()['depth']
    theme = useComponentTheme('UnorderedList')
    styles = theme['styles']
    config = theme['config']
    next_list_context = {'depth': depth + 1}
    marker = config().get('marker')
    if isinstance(marker, str):
        next_item_context = {'marker': marker}
    elif isinstance(marker, list):
        next_item_context = {'marker': marker[depth] if depth < len(marker) else (marker[-1] if marker else defaultMarker)}
    else:
        next_item_context = {'marker': defaultMarker}

    content = Box(*children, **styles['list']())
    return createElement(
        cast(Any, unorderedListContext.Provider),
        createElement(
            cast(Any, unorderedListItemContext.Provider),
            content,
            value=next_item_context,
        ),
        value=next_list_context,
    )


def _unordered_list(*children: Any) -> Any:
    return createElement(_UnorderedList, *children)


UnorderedList = cast(_ListComponent, _unordered_list)
UnorderedList.Item = UnorderedListItem
