import _bootstrap  # noqa: F401

from pyinkui import Box, ConfirmInput, Text, render
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
