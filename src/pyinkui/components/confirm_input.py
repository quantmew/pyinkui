from pyinkcli import Text, useInput
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
    def handleInput(input, key):
        lowered = input.lower() if input else input
        if lowered == 'y':
            onConfirm()
        if lowered == 'n':
            onCancel()
        if key.return_pressed and submitOnEnter:
            if defaultChoice == 'confirm':
                onConfirm()
            else:
                onCancel()

    useInput(handleInput, is_active=not isDisabled)
    styles = useComponentTheme('ConfirmInput')['styles']
    return Text('Y/n' if defaultChoice == 'confirm' else 'y/N', **styles['input']({'isFocused': not isDisabled}))


def ConfirmInput(*, isDisabled=False, defaultChoice='confirm', submitOnEnter=True, onConfirm, onCancel):
    return createElement(
        _ConfirmInput,
        isDisabled=isDisabled,
        defaultChoice=defaultChoice,
        submitOnEnter=submitOnEnter,
        onConfirm=onConfirm,
        onCancel=onCancel,
    )
