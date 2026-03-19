# Alert

> `Alert` is used to focus user's attention to important messages.

[Example code](../examples/alert.py)

## Usage

```python
from pyinkcli import Box, render
from pyinkui import Alert


def App():
    return Box(
        Alert('A new version of this CLI is available', variant='success'),
        Alert('Your license is expired', variant='error'),
        Alert('Current version of this CLI has been deprecated', variant='warning'),
        Alert('API won't be available tomorrow night', variant='info'),
        flexDirection='column',
        width=60,
    )


if __name__ == '__main__':
    render(App).wait_until_exit()
```

<img src="../media/alert.png" width="600">

## Props

### children

Type: `ReactNode`

Message.

### variant

Type: `'info' | 'success' | 'error' | 'warning'`

Variant, which determines the color of the alert.

### title

Type: `string`

Title to show above the message.
