from __future__ import annotations

from pyinkcli import Text, useInput
from pyinkcli.component import createElement
from pyinkcli.hooks._runtime import useCallback, useEffect, useMemo, useReducer
from pyinkui._ansi import dim, inverse
from pyinkui.theme import useComponentTheme

cursor = inverse(' ')


def _reducer(state, action):
    if action['type'] == 'move-cursor-left':
        return {**state, 'cursorOffset': max(0, state['cursorOffset'] - 1)}
    if action['type'] == 'move-cursor-right':
        return {**state, 'cursorOffset': min(len(state['value']), state['cursorOffset'] + 1)}
    if action['type'] == 'insert':
        return {
            **state,
            'previousValue': state['value'],
            'value': state['value'][: state['cursorOffset']] + action['text'] + state['value'][state['cursorOffset'] :],
            'cursorOffset': state['cursorOffset'] + len(action['text']),
        }
    if action['type'] == 'delete':
        newCursorOffset = max(0, state['cursorOffset'] - 1)
        return {
            **state,
            'previousValue': state['value'],
            'value': state['value'][:newCursorOffset] + state['value'][newCursorOffset + 1 :],
            'cursorOffset': newCursorOffset,
        }
    return state


def usePasswordInputState(*, onChange=None, onSubmit=None):
    state, dispatch = useReducer(_reducer, {'previousValue': '', 'value': '', 'cursorOffset': 0})
    moveCursorLeft = useCallback(lambda: dispatch({'type': 'move-cursor-left'}), ())
    moveCursorRight = useCallback(lambda: dispatch({'type': 'move-cursor-right'}), ())
    insert = useCallback(lambda text: dispatch({'type': 'insert', 'text': text}), ())
    delete = useCallback(lambda: dispatch({'type': 'delete'}), ())
    submit = useCallback(lambda: onSubmit(state['value']) if onSubmit else None, (state['value'], onSubmit))

    def emitChange():
        if state['value'] != state['previousValue'] and onChange:
            onChange(state['value'])
    useEffect(lambda: (emitChange(), None)[1], (state['previousValue'], state['value'], onChange))

    return {**state, 'moveCursorLeft': moveCursorLeft, 'moveCursorRight': moveCursorRight, 'insert': insert, 'delete': delete, 'submit': submit}


def usePasswordInput(*, isDisabled=False, state, placeholder=''):
    renderedPlaceholder = useMemo(lambda: dim(placeholder) if (isDisabled and placeholder) else (inverse(placeholder[0]) + dim(placeholder[1:]) if placeholder else cursor), (isDisabled, placeholder))

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


def _PasswordInput(*, isDisabled=False, placeholder='', onChange=None, onSubmit=None):
    state = usePasswordInputState(onChange=onChange, onSubmit=onSubmit)
    inputValue = usePasswordInput(isDisabled=isDisabled, placeholder=placeholder, state=state)['inputValue']
    styles = useComponentTheme('PasswordInput')['styles']
    return Text(inputValue, **styles['value']())


def PasswordInput(*, isDisabled=False, placeholder='', onChange=None, onSubmit=None):
    return createElement(
        _PasswordInput,
        isDisabled=isDisabled,
        placeholder=placeholder,
        onChange=onChange,
        onSubmit=onSubmit,
    )
