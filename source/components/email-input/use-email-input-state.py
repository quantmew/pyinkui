from __future__ import annotations

from pyinkcli.hooks._runtime import useCallback, useEffect, useMemo, useReducer


def reducer(state, action):
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
    state, dispatch = useReducer(
        reducer,
        {
            'previousValue': defaultValue,
            'value': defaultValue,
            'cursorOffset': len(defaultValue),
        },
    )

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

    return {
        **state,
        'suggestion': suggestion,
        'moveCursorLeft': moveCursorLeft,
        'moveCursorRight': moveCursorRight,
        'insert': insert,
        'delete': delete,
        'submit': submit,
    }
