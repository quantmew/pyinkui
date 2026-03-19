from __future__ import annotations

from pyinkcli import Box, Text
from pyinkcli.component import createElement
from pyinkui.theme import useComponentTheme

from pyinkui.components.spinner import useSpinner


def _Spinner(*, label=None, spinnerType='dots'):
    frame = useSpinner(type=spinnerType)['frame']
    styles = useComponentTheme('Spinner')['styles']
    children = [Text(frame, **styles['frame']())]
    if label:
        children.append(Text(label, **styles['label']()))
    return Box(*children, **styles['container']())


def Spinner(*, label=None, type='dots'):
    return createElement(_Spinner, label=label, spinnerType=type)
