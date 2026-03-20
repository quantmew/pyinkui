from pyinkcli import Box, Text
from pyinkcli.component import createElement
from pyinkui.theme import useComponentTheme


def _ConfirmInput(*, onConfirm, onCancel):
    styles = useComponentTheme('ConfirmInput')['styles']
    return Box(
        Text('(Y/n)', **styles['input']({'isFocused': True})),
    )


def ConfirmInput(*, onConfirm, onCancel):
    return createElement(_ConfirmInput, onConfirm=onConfirm, onCancel=onCancel)
