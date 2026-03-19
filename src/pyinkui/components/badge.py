from pyinkcli import Text
from pyinkcli.component import createElement
from pyinkui.theme import useComponentTheme


def _Badge(*children, color='magenta'):
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


def Badge(*children, color='magenta'):
    return createElement(_Badge, *children, color=color)
