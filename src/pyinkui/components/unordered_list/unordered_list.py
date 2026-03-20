from __future__ import annotations

from typing import Any, Callable, Protocol, cast

from pyinkcli import Box, Text
from pyinkcli._component_runtime import scopeRender
from pyinkcli.component import createElement
from pyinkui._contexts import getUnorderedListContext, getUnorderedListItemContext, provideUnorderedListContext, provideUnorderedListItemContext
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
    listContext = {'depth': depth + 1}
    marker = config().get('marker')
    if isinstance(marker, str):
        listItemContext = {'marker': marker}
    elif isinstance(marker, list):
        listItemContext = {'marker': marker[depth] if depth < len(marker) else (marker[-1] if marker else defaultMarker)}
    else:
        listItemContext = {'marker': defaultMarker}
    return scopeRender(
        Box(*children, **styles['list']()),
        lambda: provideUnorderedListContext(listContext),
        lambda: provideUnorderedListItemContext(listItemContext),
    )


def _unordered_list(*children: Any) -> Any:
    return createElement(_UnorderedList, *children)


UnorderedList = cast(_ListComponent, _unordered_list)
UnorderedList.Item = UnorderedListItem
