from pyinkcli import Box, Text, render
from pyinkui import Select
from pyinkcli.hooks import useState


def App():
    value, setValue = useState(None)
    return Box(
        Select(
            options=[
                {'label': 'Red', 'value': 'red'},
                {'label': 'Green', 'value': 'green'},
                {'label': 'Yellow', 'value': 'yellow'},
                {'label': 'Blue', 'value': 'blue'},
                {'label': 'Magenta', 'value': 'magenta'},
                {'label': 'Cyan', 'value': 'cyan'},
                {'label': 'White', 'value': 'white'},
            ],
            onChange=setValue,
        ),
        Text(f'Selected value: {value}'),
        flex_direction='column',
        padding=2,
        gap=1,
    )


if __name__ == '__main__':
    render(App).wait_until_exit()
