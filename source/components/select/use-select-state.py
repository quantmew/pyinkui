from __future__ import annotations

from pyinkcli.hooks._runtime import useCallback, useEffect, useMemo, useReducer, useState
from pyinkui.lib.option_map import OptionMap


def reducer(state, action):
    if action['type'] == 'focus-next-option':
        if not state['focusedValue']:
            return state
        item = state['optionMap'].get(state['focusedValue'])
        if not item or not item.next:
            return state
        next = item.next
        needsToScroll = next.index >= state['visibleToIndex']
        if not needsToScroll:
            return {**state, 'focusedValue': next.value}
        nextVisibleToIndex = min(len(state['optionMap']), state['visibleToIndex'] + 1)
        nextVisibleFromIndex = nextVisibleToIndex - state['visibleOptionCount']
        return {**state, 'focusedValue': next.value, 'visibleFromIndex': nextVisibleFromIndex, 'visibleToIndex': nextVisibleToIndex}
    if action['type'] == 'focus-previous-option':
        if not state['focusedValue']:
            return state
        item = state['optionMap'].get(state['focusedValue'])
        if not item or not item.previous:
            return state
        previous = item.previous
        needsToScroll = previous.index <= state['visibleFromIndex']
        if not needsToScroll:
            return {**state, 'focusedValue': previous.value}
        nextVisibleFromIndex = max(0, state['visibleFromIndex'] - 1)
        nextVisibleToIndex = nextVisibleFromIndex + state['visibleOptionCount']
        return {**state, 'focusedValue': previous.value, 'visibleFromIndex': nextVisibleFromIndex, 'visibleToIndex': nextVisibleToIndex}
    if action['type'] == 'select-focused-option':
        return {**state, 'previousValue': state['value'], 'value': state['focusedValue']}
    if action['type'] == 'reset':
        return action['state']
    return state


def createDefaultState(*, visibleOptionCount, defaultValue, options):
    visibleOptionCount = min(visibleOptionCount, len(options)) if isinstance(visibleOptionCount, int) else len(options)
    optionMap = OptionMap(options)
    return {
        'optionMap': optionMap,
        'visibleOptionCount': visibleOptionCount,
        'focusedValue': optionMap.first.value if optionMap.first else None,
        'visibleFromIndex': 0,
        'visibleToIndex': visibleOptionCount,
        'previousValue': defaultValue,
        'value': defaultValue,
    }


def useSelectState(*, visibleOptionCount=5, options, defaultValue=None, onChange=None):
    state, dispatch = useReducer(
        reducer,
        {'visibleOptionCount': visibleOptionCount, 'defaultValue': defaultValue, 'options': options},
        lambda initial: createDefaultState(**initial),
    )
    lastOptions, setLastOptions = useState(options)
    if options is not lastOptions and options != lastOptions:
        dispatch({'type': 'reset', 'state': createDefaultState(visibleOptionCount=visibleOptionCount, defaultValue=defaultValue, options=options)})
        setLastOptions(options)

    focusNextOption = useCallback(lambda: dispatch({'type': 'focus-next-option'}), ())
    focusPreviousOption = useCallback(lambda: dispatch({'type': 'focus-previous-option'}), ())
    selectFocusedOption = useCallback(lambda: dispatch({'type': 'select-focused-option'}), ())
    visibleOptions = useMemo(
        lambda: [{**option, 'index': index} for index, option in enumerate(options)][state['visibleFromIndex'] : state['visibleToIndex']],
        (tuple((o['label'], o['value']) for o in options), state['visibleFromIndex'], state['visibleToIndex']),
    )

    def emitChange():
        if state['value'] and state['previousValue'] != state['value'] and onChange:
            onChange(state['value'])

    useEffect(lambda: (emitChange(), None)[1], (state['previousValue'], state['value'], tuple((o['label'], o['value']) for o in options), onChange))

    return {
        'focusedValue': state['focusedValue'],
        'visibleFromIndex': state['visibleFromIndex'],
        'visibleToIndex': state['visibleToIndex'],
        'value': state['value'],
        'visibleOptions': visibleOptions,
        'focusNextOption': focusNextOption,
        'focusPreviousOption': focusPreviousOption,
        'selectFocusedOption': selectFocusedOption,
    }
