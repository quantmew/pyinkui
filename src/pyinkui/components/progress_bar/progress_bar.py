from __future__ import annotations

from typing import Any, cast

from pyinkcli import Box, Text, measureElement
from pyinkcli.component import createElement
from pyinkcli.hooks._runtime import useState
from pyinkui.theme import useComponentTheme

measureElement_ = cast(Any, measureElement)
useState_ = cast(Any, useState)


def _ProgressBar(*, value: int | float) -> Any:
    width, setWidth = useState_(0)
    ref, setRef = useState_(None)

    if ref is not None:
        dimensions = measureElement_(ref)
        measured_width = dimensions.width
        if measured_width == 0:
            parent = getattr(ref, 'parentNode', None)
            if parent is not None:
                measured_width = measureElement_(parent).width
        if measured_width != width:
            setWidth(measured_width)

    progress = min(100, max(0, value))
    complete = round((progress / 100) * width)
    remaining = width - complete
    theme = useComponentTheme('ProgressBar')
    styles = theme['styles']
    config = theme['config']
    children = []
    if complete > 0:
        children.append(Text(config()['completedCharacter'] * complete, **styles['completed']()))
    if remaining > 0:
        children.append(Text(config()['remainingCharacter'] * remaining, **styles['remaining']()))

    return Box(*children, ref=setRef, **styles['container']())


def ProgressBar(*, value: int | float) -> Any:
    return createElement(_ProgressBar, value=value)
