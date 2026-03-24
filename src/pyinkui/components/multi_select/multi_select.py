from __future__ import annotations

from pyinkcli import Box, Text, useInput
from pyinkcli.component import createElement
from pyinkcli.hooks._runtime import useCallback, useEffect, useMemo, useReducer, useState
from pyinkui._figures import pointer, tick
from pyinkui.lib.option_map import OptionMap
from pyinkui.theme import useComponentTheme


def _reducer(state, action):
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
    if action['type'] == 'toggle-focused-option':
        if not state['focusedValue']:
            return state
        if state['focusedValue'] in state['value']:
            newValue = [item for item in state['value'] if item != state['focusedValue']]
            return {**state, 'previousValue': state['value'], 'value': newValue}
        return {**state, 'previousValue': state['value'], 'value': [*state['value'], state['focusedValue']]}
    if action['type'] == 'reset':
        return action['state']
    return state


def _createDefaultState(*, visibleOptionCount, defaultValue, options):
    visibleOptionCount = min(visibleOptionCount, len(options)) if isinstance(visibleOptionCount, int) else len(options)
    optionMap = OptionMap(options)
    value = defaultValue or []
    return {
        'optionMap': optionMap,
        'visibleOptionCount': visibleOptionCount,
        'focusedValue': optionMap.first.value if optionMap.first else None,
        'visibleFromIndex': 0,
        'visibleToIndex': visibleOptionCount,
        'previousValue': value,
        'value': value,
    }


def useMultiSelectState(*, visibleOptionCount=5, options, defaultValue=None, onChange=None, onSubmit=None):
    state, dispatch = useReducer(_reducer, {'visibleOptionCount': visibleOptionCount, 'defaultValue': defaultValue, 'options': options}, lambda initial: _createDefaultState(**initial))
    lastOptions, setLastOptions = useState(options)
    if options is not lastOptions and options != lastOptions:
        dispatch({'type': 'reset', 'state': _createDefaultState(visibleOptionCount=visibleOptionCount, defaultValue=defaultValue, options=options)})
        setLastOptions(options)
    focusNextOption = useCallback(lambda: dispatch({'type': 'focus-next-option'}), ())
    focusPreviousOption = useCallback(lambda: dispatch({'type': 'focus-previous-option'}), ())
    toggleFocusedOption = useCallback(lambda: dispatch({'type': 'toggle-focused-option'}), ())
    submit = useCallback(lambda: onSubmit(state['value']) if onSubmit else None, (tuple(state['value']), onSubmit))
    visibleOptions = useMemo(lambda: [{**option, 'index': index} for index, option in enumerate(options)][state['visibleFromIndex'] : state['visibleToIndex']], (tuple((o['label'], o['value']) for o in options), state['visibleFromIndex'], state['visibleToIndex']))

    def emitChange():
        if state['previousValue'] != state['value'] and onChange:
            onChange(state['value'])
    useEffect(lambda: (emitChange(), None)[1], (tuple(state['previousValue']), tuple(state['value']), tuple((o['label'], o['value']) for o in options), onChange))
    return {
        'focusedValue': state['focusedValue'],
        'visibleFromIndex': state['visibleFromIndex'],
        'visibleToIndex': state['visibleToIndex'],
        'value': state['value'],
        'visibleOptions': visibleOptions,
        'focusNextOption': focusNextOption,
        'focusPreviousOption': focusPreviousOption,
        'toggleFocusedOption': toggleFocusedOption,
        'submit': submit,
    }


def useMultiSelect(*, isDisabled=False, state):
    def handleInput(input, key):
        if isDisabled:
            return
        if key.down_arrow:
            state['focusNextOption']()
        if key.up_arrow:
            state['focusPreviousOption']()
        if input == ' ':
            state['toggleFocusedOption']()
        if key.return_pressed or input in ('\r', '\n'):
            state['submit']()
    useInput(handleInput)


def _MultiSelectOption(*children, isFocused, isSelected):
    styles = useComponentTheme('MultiSelect')['styles']
    nodes = []
    if isFocused:
        nodes.append(Text(pointer, **styles['focusIndicator']()))
    nodes.append(Text(*children, **styles['label']({'isFocused': isFocused, 'isSelected': isSelected})))
    if isSelected:
        nodes.append(Text(tick, **styles['selectedIndicator']()))
    return Box(*nodes, **styles['option']({'isFocused': isFocused}))


def MultiSelectOption(*children, isFocused, isSelected):
    return createElement(_MultiSelectOption, *children, isFocused=isFocused, isSelected=isSelected)


def _MultiSelect(*, isDisabled=False, visibleOptionCount=5, highlightText=None, options, defaultValue=None, onChange=None, onSubmit=None):
    state = useMultiSelectState(visibleOptionCount=visibleOptionCount, options=options, defaultValue=defaultValue, onChange=onChange, onSubmit=onSubmit)
    useMultiSelect(isDisabled=isDisabled, state=state)
    styles = useComponentTheme('MultiSelect')['styles']
    children = []
    for option in state['visibleOptions']:
        label = option['label']
        if highlightText and highlightText in option['label']:
            index = option['label'].index(highlightText)
            label = [option['label'][:index], Text(highlightText, **styles['highlightedText']()), option['label'][index + len(highlightText) :]]
        children.append(MultiSelectOption(label, isFocused=(not isDisabled and state['focusedValue'] == option['value']), isSelected=(option['value'] in state['value'])))
    return Box(*children, **styles['container']())


def MultiSelect(*, isDisabled=False, visibleOptionCount=5, highlightText=None, options=None, defaultValue=None, onChange=None, onSubmit=None):
    return createElement(
        _MultiSelect,
        isDisabled=isDisabled,
        visibleOptionCount=visibleOptionCount,
        highlightText=highlightText,
        options=options or [],
        defaultValue=defaultValue,
        onChange=onChange,
        onSubmit=onSubmit,
    )
