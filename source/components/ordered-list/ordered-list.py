from pyinkcli import Box
from pyinkcli.component import isElement
from pyinkcli._component_runtime import scopeRender
from pyinkui._contexts import getOrderedListContext, provideOrderedListContext, provideOrderedListItemContext
from pyinkui.theme import useComponentTheme
from pyinkui.components.ordered_list import OrderedListItem


def OrderedList(*children):
    parentMarker = getOrderedListContext()['marker']
    styles = useComponentTheme('OrderedList')['styles']
    numberOfItems = 0

    for child in children:
        if isElement(child) and getattr(child, 'type', None) is OrderedListItem:
            numberOfItems += 1

    maxMarkerWidth = len(str(numberOfItems))
    wrappedChildren = []
    itemIndex = 0

    for child in children:
        if not (isElement(child) and getattr(child, 'type', None) is OrderedListItem):
            wrappedChildren.append(child)
            continue

        itemIndex += 1
        paddedMarker = f"{str(itemIndex).rjust(maxMarkerWidth)}."
        marker = f"{parentMarker}{paddedMarker}"
        wrappedChildren.append(
            scopeRender(
                child,
                lambda marker=marker: provideOrderedListContext({'marker': marker}),
                lambda marker=marker: provideOrderedListItemContext({'marker': marker}),
            )
        )

    return Box(*wrappedChildren, **styles['list']())


OrderedList.Item = OrderedListItem

__all__ = ['OrderedList']
