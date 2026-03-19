from typing import TypedDict

from pyinkui._figures import line


class OrderedListItemContextProps(TypedDict):
    marker: str


OrderedListItemContext: OrderedListItemContextProps = {
    'marker': line,
}
