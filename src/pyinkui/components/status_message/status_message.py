from __future__ import annotations

from typing import Any

from pyinkcli import Box, Text
from pyinkcli.component import createElement
from pyinkui.theme import useComponentTheme

StatusMessageVariant = str


def _StatusMessage(*children: Any, variant: StatusMessageVariant) -> Any:
    theme = useComponentTheme('StatusMessage')
    styles = theme['styles']
    config = theme['config']
    return Box(
        Box(Text(f"{config({'variant': variant})['icon']} ", **styles['icon']({'variant': variant})), **styles['iconContainer']()),
        Text(*children, **styles['message']()),
        **styles['container'](),
    )


def StatusMessage(*children: Any, variant: StatusMessageVariant) -> Any:
    return createElement(_StatusMessage, *children, variant=variant)
