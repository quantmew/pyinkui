from pyinkcli import Box, Text
from pyinkcli.component import createElement
from pyinkui.theme import useComponentTheme


def _Alert(*children, variant, title=None):
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


def Alert(*children, variant, title=None):
    return createElement(_Alert, *children, variant=variant, title=title)
