from pyinkcli import Box, Text, render
from pyinkui import EmailInput
from pyinkcli.hooks import useState


def App():
    value, setValue = useState('')
    return Box(
        EmailInput(placeholder='Enter email...', onChange=setValue),
        Text(f'Input value: "{value}"'),
        flexDirection='column',
        padding=2,
        gap=1,
    )


if __name__ == '__main__':
    render(App, interactive=True).wait_until_exit()
