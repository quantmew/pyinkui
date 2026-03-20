from pyinkcli import Box, Text
from pyinkcli.component import createElement
from pyinkcli.component import isElement
from pyinkcli._component_runtime import scopeRender
from pyinkui._contexts import getOrderedListContext, getOrderedListItemContext, provideOrderedListContext, provideOrderedListItemContext
from pyinkui._figures import line
from pyinkui.theme import useComponentTheme


def _OrderedListItem(*children):
    marker = getOrderedListItemContext()['marker']
    styles = useComponentTheme('OrderedList')['styles']
    return Box(Text(marker, **styles['marker']()), Box(*children, **styles['content']()), **styles['listItem']())


def OrderedListItem(*children):
    return createElement(_OrderedListItem, *children)


def _OrderedList(*children):
    parentMarker = getOrderedListContext()['marker']
    styles = useComponentTheme('OrderedList')['styles']
    numberOfItems = 0
    for child in children:
        if isElement(child) and getattr(child, 'type', None) is _OrderedListItem:
            numberOfItems += 1
    maxMarkerWidth = len(str(numberOfItems))
    wrappedChildren = []
    itemIndex = 0
    for child in children:
        if not (isElement(child) and getattr(child, 'type', None) is _OrderedListItem):
            wrappedChildren.append(child)
            continue
        itemIndex += 1
        paddedMarker = f"{str(itemIndex).rjust(maxMarkerWidth)}."
        marker = f"{parentMarker}{paddedMarker}"
        wrappedChildren.append(scopeRender(child, lambda marker=marker: provideOrderedListContext({'marker': marker}), lambda marker=marker: provideOrderedListItemContext({'marker': marker})))
    return Box(*wrappedChildren, **styles['list']())


def OrderedList(*children):
    return createElement(_OrderedList, *children)


OrderedList.Item = OrderedListItem
