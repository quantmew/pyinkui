from pyinkcli import Box, Text, measureElement
from pyinkcli.component import createElement
from pyinkcli.hooks._runtime import useState
from pyinkui.theme import useComponentTheme


def _ProgressBar(*, value):
    width, setWidth = useState(0)
    ref, setRef = useState(None)

    if ref is not None:
        dimensions = measureElement(ref)
        measured_width = dimensions.width
        if measured_width == 0:
            parent = getattr(ref, 'parentNode', None)
            if parent is not None:
                measured_width = measureElement(parent).width
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


def ProgressBar(*, value):
    return createElement(_ProgressBar, value=value)
