# Text input

> `TextInput` is used for entering any single-line input with an optional autocomplete.

[Example code](../examples/text-input.py)

## Usage

```python
from pyinkui import TextInput, render


def App():
    return TextInput(placeholder='Start typing...')


if __name__ == '__main__':
    render(App).wait_until_exit()
```
