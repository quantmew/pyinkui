from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from pyinkui.types import Option


@dataclass
class OptionMapItem:
    label: str
    value: str
    previous: 'OptionMapItem | None'
    next: 'OptionMapItem | None'
    index: int


class OptionMap(dict[str, OptionMapItem]):
    def __init__(self, options: Iterable[Option]):
        super().__init__()
        self.first: OptionMapItem | None = None
        previous: OptionMapItem | None = None
        for index, option in enumerate(options):
            item = OptionMapItem(
                label=option['label'],
                value=option['value'],
                previous=previous,
                next=None,
                index=index,
            )
            if previous is not None:
                previous.next = item
            if self.first is None:
                self.first = item
            self[item.value] = item
            previous = item
