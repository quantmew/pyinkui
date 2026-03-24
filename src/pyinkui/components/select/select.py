from __future__ import annotations

from typing import Any, Callable, cast

from pyinkcli import Box, Text, useInput
from pyinkcli.component import createElement
from pyinkcli.hooks._runtime import useCallback, useEffect, useMemo, useReducer, useState
from pyinkui._figures import pointer, tick
from pyinkui.lib.option_map import OptionMap
from pyinkui.types import Option
from pyinkui.theme import useComponentTheme

useCallback_ = cast(Any, useCallback)
useEffect_ = cast(Any, useEffect)
useInput_ = cast(Any, useInput)
useMemo_ = cast(Any, useMemo)
useReducer_ = cast(Any, useReducer)
useState_ = cast(Any, useState)
OptionItem = Option


def _reducer(state: dict[str, Any], action: dict[str, Any]) -> dict[str, Any]:
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
        return cast(dict[str, Any], action['state'])
    return state


def _createDefaultState(*, visibleOptionCount: int | None, defaultValue: str | None, options: list[OptionItem]) -> dict[str, Any]:
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


def useSelectState(
    *,
    visibleOptionCount: int = 5,
    options: list[OptionItem],
    defaultValue: str | None = None,
    onChange: Callable[[str], Any] | None = None,
) -> dict[str, Any]:
    state, dispatch = useReducer_(
        _reducer,
        {'visibleOptionCount': visibleOptionCount, 'defaultValue': defaultValue, 'options': options},
        lambda initial: _createDefaultState(**initial),
    )
    lastOptions, setLastOptions = useState_(options)
    if options is not lastOptions and options != lastOptions:
        dispatch({'type': 'reset', 'state': _createDefaultState(visibleOptionCount=visibleOptionCount, defaultValue=defaultValue, options=options)})
        setLastOptions(options)
    focusNextOption = useCallback_(lambda: dispatch({'type': 'focus-next-option'}), ())
    focusPreviousOption = useCallback_(lambda: dispatch({'type': 'focus-previous-option'}), ())
    selectFocusedOption = useCallback_(lambda: dispatch({'type': 'select-focused-option'}), ())
    visibleOptions = useMemo_(
        lambda: [{**option, 'index': index} for index, option in enumerate(options)][state['visibleFromIndex'] : state['visibleToIndex']],
        (tuple((o['label'], o['value']) for o in options), state['visibleFromIndex'], state['visibleToIndex']),
    )

    def emitChange() -> None:
        if state['value'] and state['previousValue'] != state['value'] and onChange:
            onChange(state['value'])
    useEffect_(lambda: emitChange(), (state['previousValue'], state['value'], tuple((o['label'], o['value']) for o in options), onChange))
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


def useSelect(*, isDisabled: bool = False, state: dict[str, Any]) -> None:
    def handleInput(_input: str, key: Any) -> None:
        if isDisabled:
            return
        if key.down_arrow:
            state['focusNextOption']()
        if key.up_arrow:
            state['focusPreviousOption']()
        if key.return_pressed or _input in ('\r', '\n'):
            state['selectFocusedOption']()
    useInput_(handleInput)


def _SelectOption(*children: Any, isFocused: bool, isSelected: bool) -> Any:
    styles = useComponentTheme('Select')['styles']
    nodes = []
    if isFocused:
        nodes.append(Text(pointer, **styles['focusIndicator']()))
    nodes.append(Text(*children, **styles['label']({'isFocused': isFocused, 'isSelected': isSelected})))
    if isSelected:
        nodes.append(Text(tick, **styles['selectedIndicator']()))
    return Box(*nodes, **styles['option']({'isFocused': isFocused}))


def SelectOption(*children: Any, isFocused: bool, isSelected: bool) -> Any:
    return createElement(_SelectOption, *children, isFocused=isFocused, isSelected=isSelected)


def _Select(
    *,
    isDisabled: bool = False,
    visibleOptionCount: int = 5,
    highlightText: str | None = None,
    options: list[OptionItem] | None = None,
    defaultValue: str | None = None,
    onChange: Callable[[str], Any] | None = None,
) -> Any:
    options = options or []
    state = useSelectState(visibleOptionCount=visibleOptionCount, options=options, defaultValue=defaultValue, onChange=onChange)
    useSelect(isDisabled=isDisabled, state=state)
    styles = useComponentTheme('Select')['styles']
    children = []
    for option in state['visibleOptions']:
        label = option['label']
        if highlightText and highlightText in option['label']:
            index = option['label'].index(highlightText)
            label = [option['label'][:index], Text(highlightText, **styles['highlightedText']()), option['label'][index + len(highlightText) :]]
        children.append(SelectOption(label, isFocused=(not isDisabled and state['focusedValue'] == option['value']), isSelected=(state['value'] == option['value'])))
    return Box(*children, **styles['container']())


def Select(
    *,
    isDisabled: bool = False,
    visibleOptionCount: int = 5,
    highlightText: str | None = None,
    options: list[OptionItem] | None = None,
    defaultValue: str | None = None,
    onChange: Callable[[str], Any] | None = None,
) -> Any:
    return createElement(
        _Select,
        isDisabled=isDisabled,
        visibleOptionCount=visibleOptionCount,
        highlightText=highlightText,
        options=options or [],
        defaultValue=defaultValue,
        onChange=onChange,
    )
