from __future__ import annotations

from pyinkcli.hooks._runtime import useCallback, useEffect, useReducer


def reducer(state, action):
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
    state, dispatch = useReducer(reducer, {'previousValue': '', 'value': '', 'cursorOffset': 0})
    moveCursorLeft = useCallback(lambda: dispatch({'type': 'move-cursor-left'}), ())
    moveCursorRight = useCallback(lambda: dispatch({'type': 'move-cursor-right'}), ())
    insert = useCallback(lambda text: dispatch({'type': 'insert', 'text': text}), ())
    delete = useCallback(lambda: dispatch({'type': 'delete'}), ())
    submit = useCallback(lambda: onSubmit(state['value']) if onSubmit else None, (state['value'], onSubmit))

    def emitChange():
        if state['value'] != state['previousValue'] and onChange:
            onChange(state['value'])

    useEffect(lambda: (emitChange(), None)[1], (state['previousValue'], state['value'], onChange))

    return {
        **state,
        'moveCursorLeft': moveCursorLeft,
        'moveCursorRight': moveCursorRight,
        'insert': insert,
        'delete': delete,
        'submit': submit,
    }
