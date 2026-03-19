from typing import TypedDict


class UnorderedListContextProps(TypedDict):
    depth: int


UnorderedListContext: UnorderedListContextProps = {
    'depth': 0,
}
