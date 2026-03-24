from __future__ import annotations

from typing import Any

from pyinkcli import Text
from pyinkcli.component import createElement
from pyinkui.theme import useComponentTheme


def _Badge(*children: Any, color: str = 'magenta') -> Any:
    styles = useComponentTheme('Badge')['styles']
    formattedChildren = children[0] if len(children) == 1 else children
    if isinstance(formattedChildren, str):
        formattedChildren = formattedChildren.upper()
    return Text(
        ' ',
        Text(formattedChildren, **styles['label']()),
        ' ',
        **styles['container']({'color': color}),
    )


def Badge(*children: Any, color: str = 'magenta') -> Any:
    return createElement(_Badge, *children, color=color)
