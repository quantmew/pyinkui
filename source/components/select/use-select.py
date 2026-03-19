from pyinkcli import useInput


def useSelect(*, isDisabled=False, state):
    def handleInput(_input, key):
        if key.down_arrow:
            state['focusNextOption']()
        if key.up_arrow:
            state['focusPreviousOption']()
        if key.return_pressed:
            state['selectFocusedOption']()

    useInput(handleInput, is_active=not isDisabled)
