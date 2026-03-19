from pyinkcli import Box, Text
from pyinkui._contexts import getUnorderedListItemContext
from pyinkui.theme import useComponentTheme


def UnorderedListItem(*children):
    marker = getUnorderedListItemContext()['marker']
    styles = useComponentTheme('UnorderedList')['styles']
    return Box(
        Text(marker, **styles['marker']()),
        Box(*children, **styles['content']()),
        **styles['listItem'](),
    )


__all__ = ['UnorderedListItem']
