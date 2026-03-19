# Select

> `Select` shows a scrollable list of options for a user to choose from.

[Example code](../examples/select.py)

## Usage

```python
from pyinkui import Select, render

options = [
    {'label': 'Red', 'value': 'red'},
    {'label': 'Green', 'value': 'green'},
    {'label': 'Blue', 'value': 'blue'},
]


def App():
    return Select(options=options)


if __name__ == '__main__':
    render(App).wait_until_exit()
```
