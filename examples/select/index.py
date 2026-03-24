import sys
from pathlib import Path

from pyinkcli import Box, Text, render
from pyinkcli.hooks import useState
from pyinkui import Select


ROOT = Path(__file__).resolve().parents[2]
CLI_SRC = ROOT.parent / 'pyinkcli' / 'src'
UI_SRC = ROOT / 'src'

for candidate in (str(CLI_SRC), str(UI_SRC)):
    if candidate not in sys.path:
        sys.path.insert(0, candidate)


def App():
    value, setValue = useState('')
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
        flexDirection='column',
        padding=2,
        gap=1,
    )


if __name__ == '__main__':
    render(App, interactive=True).wait_until_exit()
