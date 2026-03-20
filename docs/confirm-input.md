# Confirm input

> `ConfirmInput` shows a common "(Y/n)" input to confirm or cancel an operation your CLI wants to perform.

[Example code](../examples/confirm-input.py)

## Usage

```python
from pyinkcli import Box, Text, render
from pyinkui import ConfirmInput
from pyinkcli.hooks import useState


def App():
    status, setStatus = useState('Waiting for confirmation')
    return Box(
        Text(status),
        ConfirmInput(
            onConfirm=lambda: setStatus('Confirmed'),
            onCancel=lambda: setStatus('Cancelled'),
        ),
        flexDirection='column',
    )


if __name__ == '__main__':
    render(App).wait_until_exit()
```

## Props

### isDisabled

Type: `boolean`\
Default: `false`

When disabled, user input is ignored.

### defaultChoice

Type: `'confirm' | 'cancel'`\
Default: `'confirm'`

Default choice.

### submitOnEnter

Type: `boolean`\
Default: `true`

Confirm or cancel when user presses enter, depending on the `defaultChoice` value.
Can be useful to disable when an explicit confirmation is required, such as pressing <kbd>Y</kbd> key.

### onConfirm

Type: `Function`

Callback to trigger on confirmation.

### onCancel

Type: `Function`

Callback to trigger on cancellation.
