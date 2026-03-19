from pyinkcli import Box, Text
from pyinkui.components.select import SelectOption, useSelect, useSelectState
from pyinkui.theme import useComponentTheme


def Select(
    *,
    isDisabled=False,
    visibleOptionCount=5,
    highlightText=None,
    options,
    defaultValue=None,
    onChange=None,
):
    state = useSelectState(
        visibleOptionCount=visibleOptionCount,
        options=options,
        defaultValue=defaultValue,
        onChange=onChange,
    )
    useSelect(isDisabled=isDisabled, state=state)
    styles = useComponentTheme('Select')['styles']
    children = []

    for option in state['visibleOptions']:
        label = option['label']

        if highlightText and highlightText in option['label']:
            index = option['label'].index(highlightText)
            label = [
                option['label'][:index],
                Text(highlightText, **styles['highlightedText']()),
                option['label'][index + len(highlightText) :],
            ]

        children.append(
            SelectOption(
                label,
                isFocused=(not isDisabled and state['focusedValue'] == option['value']),
                isSelected=(state['value'] == option['value']),
            )
        )

    return Box(*children, **styles['container']())


__all__ = ['Select']
