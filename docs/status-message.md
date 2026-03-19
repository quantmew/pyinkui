# Status message

> `StatusMessage` can also be used to indicate a status, but when longer explanation of such status is required.

[Example code](../examples/status-message.py)

## Usage

```python
from pyinkui import StatusMessage, render


def App():
    return StatusMessage('Ready', variant='success')


if __name__ == '__main__':
    render(App).wait_until_exit()
```

<img src="../media/status-message.png" width="400">

## Props

### children

Type: `ReactNode`

Message.

### variant

Type: `'info' | 'success' | 'error' | 'warning'`

Variant, which determines the color used in the status message.
