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
        if '@' in state['value'] and '@' in action['text']:
            return state
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


def useEmailInputState(*, defaultValue='', domains=None, onChange=None, onSubmit=None):
    if domains is None:
        domains = ['aol.com', 'gmail.com', 'yahoo.com', 'hotmail.com', 'live.com', 'outlook.com', 'icloud.com', 'hey.com']
    state, dispatch = useReducer(_reducer, {'previousValue': defaultValue, 'value': defaultValue, 'cursorOffset': len(defaultValue)})

    def createSuggestion():
        if len(state['value']) == 0 or '@' not in state['value']:
            return None
        atIndex = state['value'].index('@')
        enteredDomain = state['value'][atIndex + 1 :]
        for domain in domains:
            if domain.startswith(enteredDomain):
                return domain.replace(enteredDomain, '', 1)
        return None

    suggestion = useMemo(createSuggestion, (state['value'], tuple(domains)))
    moveCursorLeft = useCallback(lambda: dispatch({'type': 'move-cursor-left'}), ())
    moveCursorRight = useCallback(lambda: dispatch({'type': 'move-cursor-right'}), ())
    insert = useCallback(lambda text: dispatch({'type': 'insert', 'text': text}), ())
    delete = useCallback(lambda: dispatch({'type': 'delete'}), ())

    def submitCallback():
        if suggestion:
            insert(suggestion)
            if onSubmit:
                onSubmit(state['value'] + suggestion)
            return
        if onSubmit:
            onSubmit(state['value'])

    submit = useCallback(submitCallback, (state['value'], suggestion, insert, onSubmit))

    def emitChange():
        if state['previousValue'] != state['value'] and onChange:
            onChange(state['value'])
    useEffect(lambda: (emitChange(), None)[1], (state['previousValue'], state['value'], onChange))

    return {**state, 'suggestion': suggestion, 'moveCursorLeft': moveCursorLeft, 'moveCursorRight': moveCursorRight, 'insert': insert, 'delete': delete, 'submit': submit}


def useEmailInput(*, isDisabled=False, state, placeholder=''):
    renderedPlaceholder = useMemo(
        lambda: dim(placeholder) if (isDisabled and placeholder) else (inverse(placeholder[0]) + dim(placeholder[1:]) if placeholder else cursor),
        (isDisabled, placeholder),
    )

    def renderValue():
        if isDisabled:
            return state['value']
        index = 0
        result = '' if len(state['value']) > 0 else cursor
        for character in state['value']:
            result += inverse(character) if index == state['cursorOffset'] else character
            index += 1
        if state['suggestion']:
            if state['cursorOffset'] == len(state['value']):
                return result + inverse(state['suggestion'][0]) + dim(state['suggestion'][1:])
            return result + dim(state['suggestion'])
        if len(state['value']) > 0 and state['cursorOffset'] == len(state['value']):
            result += cursor
        return result

    renderedValue = useMemo(renderValue, (isDisabled, state['value'], state['cursorOffset'], state['suggestion']))

    def handleInput(input, key):
        if isDisabled:
            return
        if key.up_arrow or key.down_arrow or (key.ctrl and input == 'c') or key.name == 'tab':
            return
        if key.return_pressed or input in ('\r', '\n'):
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

    useInput(handleInput)
    return {'inputValue': renderedValue if len(state['value']) > 0 else renderedPlaceholder}


def _EmailInput(*, isDisabled=False, defaultValue=None, placeholder='', domains=None, onChange=None, onSubmit=None):
    state = useEmailInputState(defaultValue=defaultValue or '', domains=domains, onChange=onChange, onSubmit=onSubmit)
    inputValue = useEmailInput(isDisabled=isDisabled, placeholder=placeholder, state=state)['inputValue']
    styles = useComponentTheme('EmailInput')['styles']
    return Text(inputValue, **styles['value']())


def EmailInput(*, isDisabled=False, defaultValue=None, placeholder='', domains=None, onChange=None, onSubmit=None):
    return createElement(
        _EmailInput,
        isDisabled=isDisabled,
        defaultValue=defaultValue,
        placeholder=placeholder,
        domains=domains,
        onChange=onChange,
        onSubmit=onSubmit,
    )
