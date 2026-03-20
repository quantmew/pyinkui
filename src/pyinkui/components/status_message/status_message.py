from pyinkcli import Box, Text
from pyinkcli.component import createElement
from pyinkui.theme import useComponentTheme

StatusMessageVariant = str


def _StatusMessage(*children, variant):
    theme = useComponentTheme('StatusMessage')
    styles = theme['styles']
    config = theme['config']
    return Box(
        Box(Text(config({'variant': variant})['icon'], **styles['icon']({'variant': variant})), **styles['iconContainer']()),
        Text(*children, **styles['message']()),
        **styles['container'](),
    )


def StatusMessage(*children, variant):
    return createElement(_StatusMessage, *children, variant=variant)
