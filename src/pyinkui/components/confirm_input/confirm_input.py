from pyinkcli import Box, Text, useInput
from pyinkcli.component import createElement
from pyinkui.theme import useComponentTheme


def _ConfirmInput(*, onConfirm, onCancel):
    styles = useComponentTheme('ConfirmInput')['styles']

    def handleInput(input, key):
        if input == 'y' or input == 'Y' or key.return_pressed:
            if onConfirm:
                onConfirm()
        elif input == 'n' or input == 'N' or key.escape:
            if onCancel:
                onCancel()

    useInput(handleInput, is_active=True)

    return Box(
        Text('(Y/n)', **styles['input']({'isFocused': True})),
    )


def ConfirmInput(*, onConfirm, onCancel):
    return createElement(_ConfirmInput, onConfirm=onConfirm, onCancel=onCancel)
