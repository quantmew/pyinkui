from __future__ import annotations

from pyinkcli import useInput
from pyinkcli.hooks._runtime import useMemo
from pyinkui._ansi import dim, inverse

cursor = inverse(' ')


def usePasswordInput(*, isDisabled=False, state, placeholder=''):
    renderedPlaceholder = useMemo(
        lambda: dim(placeholder) if (isDisabled and placeholder) else (inverse(placeholder[0]) + dim(placeholder[1:]) if placeholder else cursor),
        (isDisabled, placeholder),
    )

    def renderValue():
        value = '*' * len(state['value'])
        if isDisabled:
            return value
        index = 0
        result = '' if len(value) > 0 else cursor
        for character in value:
            result += inverse(character) if index == state['cursorOffset'] else character
            index += 1
        if len(value) > 0 and state['cursorOffset'] == len(value):
            result += cursor
        return result

    renderedValue = useMemo(renderValue, (isDisabled, state['value'], state['cursorOffset']))

    def handleInput(input, key):
        if key.up_arrow or key.down_arrow or (key.ctrl and input == 'c') or key.tab or (key.shift and key.tab):
            return

        if key.return_pressed:
            state['submit']()
            return

        if key.left_arrow:
            state['moveCursorLeft']()
        elif key.right_arrow:
            state['moveCursorRight']()
        elif key.backspace or key.delete:
            state['delete']()
        elif input:
            state['insert'](input)

    useInput(handleInput, is_active=not isDisabled)
    return {'inputValue': renderedValue if len(state['value']) > 0 else renderedPlaceholder}
