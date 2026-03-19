from pyinkcli import Box
from pyinkcli._component_runtime import scopeRender
from pyinkui._contexts import getUnorderedListContext, provideUnorderedListContext, provideUnorderedListItemContext
from pyinkui._figures import line as defaultMarker
from pyinkui.theme import useComponentTheme
from pyinkui.components.unordered_list import UnorderedListItem


def UnorderedList(*children):
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


UnorderedList.Item = UnorderedListItem

__all__ = ['UnorderedList']
