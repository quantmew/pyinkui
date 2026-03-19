from pyinkcli import Box, Text
from pyinkui._figures import pointer, tick
from pyinkui.theme import useComponentTheme


def MultiSelectOption(*children, isFocused, isSelected):
    styles = useComponentTheme('MultiSelect')['styles']
    nodes = []

    if isFocused:
        nodes.append(Text(pointer, **styles['focusIndicator']()))

    nodes.append(Text(*children, **styles['label']({'isFocused': isFocused, 'isSelected': isSelected})))

    if isSelected:
        nodes.append(Text(tick, **styles['selectedIndicator']()))

    return Box(*nodes, **styles['option']({'isFocused': isFocused}))


__all__ = ['MultiSelectOption']
