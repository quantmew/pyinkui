# Ordered list

> `OrderedList` is used to show lists of numbered items.

[Example code](../examples/ordered-list.py)

## Usage

```python
from pyinkcli import Text, render
from pyinkui import OrderedList


def App():
    return OrderedList(
        OrderedList.Item(Text('Red')),
        OrderedList.Item(Text('Green')),
        OrderedList.Item(Text('Blue')),
    )


if __name__ == '__main__':
    render(App).wait_until_exit()
```

<img src="../media/ordered-list.png" width="400">

## Props

### OrderedList

#### children

Type: `ReactNode`

List items.

### OrderedList.Item

#### children

Type: `ReactNode`

List item content.
