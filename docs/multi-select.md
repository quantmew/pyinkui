# Multi select

> `MultiSelect` is similar to [`Select`](select.md), except user can choose multiple options.

[Example code](../examples/multi-select.py)

## Usage

```python
from pyinkui import MultiSelect, render

options = [
    {'label': 'Red', 'value': 'red'},
    {'label': 'Green', 'value': 'green'},
    {'label': 'Blue', 'value': 'blue'},
]


def App():
    return MultiSelect(options=options)


if __name__ == '__main__':
    render(App).wait_until_exit()
```
