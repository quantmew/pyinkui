from pyinkcli import Box, Text, useInput
from pyinkcli.component import createElement
from pyinkui.theme import useComponentTheme


def _ConfirmInput(
    *,
    isDisabled=False,
    defaultChoice='confirm',
    submitOnEnter=True,
    onConfirm,
    onCancel,
):
    styles = useComponentTheme('ConfirmInput')['styles']

    def handleInput(input, key):
        if isDisabled:
            return
        if input == 'y' or input == 'Y':
            if onConfirm:
                onConfirm()
            return
        if input == 'n' or input == 'N':
            if onCancel:
                onCancel()
            return
        if (key.return_pressed or input in ('\r', '\n')) and submitOnEnter:
            if defaultChoice == 'confirm':
                if onConfirm:
                    onConfirm()
            elif onCancel:
                onCancel()

    useInput(handleInput)

    return Box(
        Text('Y/n' if defaultChoice == 'confirm' else 'y/N', **styles['input']({'isFocused': not isDisabled})),
    )


def ConfirmInput(*, isDisabled=False, defaultChoice='confirm', submitOnEnter=True, onConfirm, onCancel):
    return createElement(
        _ConfirmInput,
        isDisabled=isDisabled,
        defaultChoice=defaultChoice,
        submitOnEnter=submitOnEnter,
        onConfirm=onConfirm,
        onCancel=onCancel,
    )
