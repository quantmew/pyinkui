from pyinkcli import Box, Text
from pyinkui.theme import useComponentTheme


def Alert(*children, variant, title=None):
    theme = useComponentTheme('Alert')
    styles = theme['styles']
    config = theme['config']
    contentChildren = []

    if title:
        contentChildren.append(Text(title, **styles['title']()))

    contentChildren.append(Text(*children, **styles['message']()))

    return Box(
        Box(Text(config({'variant': variant})['icon'], **styles['icon']({'variant': variant})), **styles['iconContainer']()),
        Box(*contentChildren, **styles['content']()),
        **styles['container']({'variant': variant}),
    )


__all__ = ['Alert']
