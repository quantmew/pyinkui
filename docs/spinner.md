# Spinner

> `Spinner` indicates that something is being processed and CLI is waiting for it to complete.

[Example code](../examples/spinner.py)

## Usage

```python
from pyinkcli import render
from pyinkui import Spinner


def App():
    return Spinner(label='Loading')


if __name__ == '__main__':
    render(App).wait_until_exit()
```

<img src="../media/spinner.gif" width="400">

## Props

### label

Type: `string`

Label to show next to the spinner.
