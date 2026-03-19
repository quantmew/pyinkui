from pyinkcli import Box, Text
from pyinkui._contexts import getOrderedListItemContext
from pyinkui.theme import useComponentTheme


def OrderedListItem(*children):
    marker = getOrderedListItemContext()['marker']
    styles = useComponentTheme('OrderedList')['styles']
    return Box(
        Text(marker, **styles['marker']()),
        Box(*children, **styles['content']()),
        **styles['listItem'](),
    )


__all__ = ['OrderedListItem']
