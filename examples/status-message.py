from pyinkcli import Box, render
from pyinkui import StatusMessage


def App():
    return Box(
        StatusMessage('Success', variant='success'),
        StatusMessage('Error', variant='error'),
        StatusMessage('Warning', variant='warning'),
        StatusMessage('Info', variant='info'),
        flexDirection='column',
        padding=2,
    )


if __name__ == '__main__':
    render(App, interactive=True).wait_until_exit()
