from __future__ import annotations

from typing import Any, Callable, cast

from pyinkcli import Text, useInput
from pyinkcli.component import createElement
from pyinkcli.hooks._runtime import useCallback, useEffect, useMemo, useReducer
from pyinkui._ansi import dim, inverse
from pyinkui.theme import useComponentTheme

useCallback_ = cast(Any, useCallback)
useEffect_ = cast(Any, useEffect)
useInput_ = cast(Any, useInput)
useMemo_ = cast(Any, useMemo)
useReducer_ = cast(Any, useReducer)
cursor = inverse(' ')


def _reducer(state: dict[str, Any], action: dict[str, Any]) -> dict[str, Any]:
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


def useTextInputState(
    *,
    defaultValue: str = '',
    suggestions: list[str] | None = None,
    onChange: Callable[[str], Any] | None = None,
    onSubmit: Callable[[str], Any] | None = None,
) -> dict[str, Any]:
    state, dispatch = useReducer_(_reducer, {
        'previousValue': defaultValue,
        'value': defaultValue,
        'cursorOffset': len(defaultValue),
    })

    def createSuggestion() -> str | None:
        if len(state['value']) == 0:
            return None
        if not suggestions:
            return None
        for suggestion in suggestions:
            if suggestion.startswith(state['value']):
                return suggestion.replace(state['value'], '', 1)
        return None

    suggestion = useMemo_(createSuggestion, (state['value'], tuple(suggestions or [])))
    moveCursorLeft = useCallback_(lambda: dispatch({'type': 'move-cursor-left'}), ())
    moveCursorRight = useCallback_(lambda: dispatch({'type': 'move-cursor-right'}), ())
    insert = useCallback_(lambda text: dispatch({'type': 'insert', 'text': text}), ())
    delete = useCallback_(lambda: dispatch({'type': 'delete'}), ())

    def submitCallback() -> None:
        if suggestion:
            insert(suggestion)
            if onSubmit:
                onSubmit(state['value'] + suggestion)
            return
        if onSubmit:
            onSubmit(state['value'])

    submit = useCallback_(submitCallback, (state['value'], suggestion, insert, onSubmit))

    def emitChange() -> None:
        if state['value'] != state['previousValue'] and onChange:
            onChange(state['value'])

    useEffect_(lambda: emitChange(), (state['previousValue'], state['value'], onChange))

    return {
        **state,
        'suggestion': suggestion,
        'moveCursorLeft': moveCursorLeft,
        'moveCursorRight': moveCursorRight,
        'insert': insert,
        'delete': delete,
        'submit': submit,
    }


def useTextInput(*, isDisabled: bool = False, state: dict[str, Any], placeholder: str = '') -> dict[str, Any]:
    def renderPlaceholder() -> str:
        if isDisabled:
            return dim(placeholder) if placeholder else ''
        return inverse(placeholder[0]) + dim(placeholder[1:]) if placeholder else cursor

    renderedPlaceholder = useMemo_(renderPlaceholder, (isDisabled, placeholder))

    def renderValue() -> str:
        if isDisabled:
            return cast(str, state['value'])
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

    renderedValue = useMemo_(renderValue, (isDisabled, state['value'], state['cursorOffset'], state['suggestion']))

    def handleInput(input: str, key: Any) -> None:
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

    useInput_(handleInput)
    return {'inputValue': renderedValue if len(state['value']) > 0 else renderedPlaceholder}


def _TextInput(
    *,
    isDisabled: bool = False,
    defaultValue: str | None = None,
    placeholder: str = '',
    suggestions: list[str] | None = None,
    onChange: Callable[[str], Any] | None = None,
    onSubmit: Callable[[str], Any] | None = None,
) -> Any:
    state = useTextInputState(defaultValue=defaultValue or '', suggestions=suggestions, onChange=onChange, onSubmit=onSubmit)
    inputValue = useTextInput(isDisabled=isDisabled, placeholder=placeholder, state=state)['inputValue']
    styles = useComponentTheme('TextInput')['styles']
    return Text(inputValue, **styles['value']())


def TextInput(
    *,
    isDisabled: bool = False,
    defaultValue: str | None = None,
    placeholder: str = '',
    suggestions: list[str] | None = None,
    onChange: Callable[[str], Any] | None = None,
    onSubmit: Callable[[str], Any] | None = None,
) -> Any:
    return createElement(
        _TextInput,
        isDisabled=isDisabled,
        defaultValue=defaultValue,
        placeholder=placeholder,
        suggestions=suggestions,
        onChange=onChange,
        onSubmit=onSubmit,
    )
