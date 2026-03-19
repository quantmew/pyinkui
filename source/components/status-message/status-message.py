from pyinkcli import Box, Text
from pyinkui.theme import useComponentTheme


def StatusMessage(*children, variant):
    theme = useComponentTheme('StatusMessage')
    styles = theme['styles']
    config = theme['config']
    return Box(
        Box(Text(config({'variant': variant})['icon'], **styles['icon']({'variant': variant})), **styles['iconContainer']()),
        Text(*children, **styles['message']()),
        **styles['container'](),
    )


__all__ = ['StatusMessage']
