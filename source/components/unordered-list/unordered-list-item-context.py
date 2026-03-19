from typing import TypedDict

from .constants import defaultMarker


class UnorderedListItemContextProps(TypedDict):
    marker: str


UnorderedListItemContext: UnorderedListItemContextProps = {
    'marker': defaultMarker,
}
