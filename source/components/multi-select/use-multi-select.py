from pyinkcli import useInput


def useMultiSelect(*, isDisabled=False, state):
    def handleInput(input, key):
        if key.down_arrow:
            state['focusNextOption']()
        if key.up_arrow:
            state['focusPreviousOption']()
        if input == ' ':
            state['toggleFocusedOption']()
        if key.return_pressed:
            state['submit']()

    useInput(handleInput, is_active=not isDisabled)
