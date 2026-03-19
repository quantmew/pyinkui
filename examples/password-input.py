from pyinkcli import Box, Text, render
from pyinkui import PasswordInput
from pyinkcli.hooks import useState


def App():
    value, setValue = useState('')
    return Box(
        PasswordInput(placeholder='Enter password...', onChange=setValue),
        Text(f'Input value: "{value}"'),
        flex_direction='column',
        padding=2,
        gap=1,
    )


if __name__ == '__main__':
    render(App).wait_until_exit()
