from pyinkcli import Box, Text
from pyinkui.components.multi_select import MultiSelectOption, useMultiSelect, useMultiSelectState
from pyinkui.theme import useComponentTheme


def MultiSelect(
    *,
    isDisabled=False,
    visibleOptionCount=5,
    highlightText=None,
    options,
    defaultValue=None,
    onChange=None,
    onSubmit=None,
):
    state = useMultiSelectState(
        visibleOptionCount=visibleOptionCount,
        options=options,
        defaultValue=defaultValue,
        onChange=onChange,
        onSubmit=onSubmit,
    )
    useMultiSelect(isDisabled=isDisabled, state=state)
    styles = useComponentTheme('MultiSelect')['styles']
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
            MultiSelectOption(
                label,
                isFocused=(not isDisabled and state['focusedValue'] == option['value']),
                isSelected=(option['value'] in state['value']),
            )
        )

    return Box(*children, **styles['container']())


__all__ = ['MultiSelect']
