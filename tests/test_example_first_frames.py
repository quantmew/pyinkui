from __future__ import annotations

from pyinkcli import Box, Text
from pyinkcli.component import createElement
from pyinkcli.hooks import useState
from pyinkui import (
    Alert,
    EmailInput,
    MultiSelect,
    PasswordInput,
    ProgressBar,
    Select,
    Spinner,
    StatusMessage,
    TextInput,
)
from tests.helpers import RenderHarness, stripAnsi

OPTIONS = [
    {'label': 'Red', 'value': 'red'},
    {'label': 'Green', 'value': 'green'},
    {'label': 'Yellow', 'value': 'yellow'},
    {'label': 'Blue', 'value': 'blue'},
    {'label': 'Magenta', 'value': 'magenta'},
    {'label': 'Cyan', 'value': 'cyan'},
    {'label': 'White', 'value': 'white'},
]


def _render_plain(node) -> str:
    harness = RenderHarness(node)
    try:
        return stripAnsi(harness.lastFrame())
    finally:
        harness.cleanup()


def test_alert_example_first_frame_matches_current_js_parity_snapshot():
    frame = _render_plain(
        Box(
            Alert('A new version of this CLI is available', variant='success'),
            Alert('Your license is expired', variant='error'),
            Alert('Current version of this CLI has been deprecated', variant='warning'),
            Alert("API won't be available tomorrow night", variant='info'),
            flexDirection='column',
            alignItems='stretch',
            padding=2,
            width=60,
            gap=1,
        )
    )

    assert frame == (
        '\n\n'
        '  ╭──────────────────────────────────────────────────────╮\n'
        '  │ ✔  A new version of this CLI is available            │\n'
        '  ╰──────────────────────────────────────────────────────╯\n\n'
        '  ╭──────────────────────────────────────────────────────╮\n'
        '  │ ✘  Your license is expired                           │\n'
        '  ╰──────────────────────────────────────────────────────╯\n\n'
        '  ╭──────────────────────────────────────────────────────╮\n'
        '  │ ⚠  Current version of this CLI has been deprecated   │\n'
        '  ╰──────────────────────────────────────────────────────╯\n\n'
        '  ╭──────────────────────────────────────────────────────╮\n'
        "  │ ℹ  API won't be available tomorrow night             │\n"
        '  ╰──────────────────────────────────────────────────────╯'
    )


def test_progress_bar_example_first_frame_matches_snapshot():
    frame = _render_plain(Box(ProgressBar(value=0), padding=2, width=30))

    assert frame == '\n\n  ░░░░░░░░░░░░░░░░░░░░░░░░░░'


def test_select_example_first_frame_matches_snapshot():
    def Example():
        value, setValue = useState('')
        return Box(
            Select(options=OPTIONS, onChange=setValue),
            Text(f'Selected value: {value}'),
            flexDirection='column',
            padding=2,
            gap=1,
        )

    frame = _render_plain(Example)

    assert frame == (
        '\n\n'
        '  ❯ Red\n'
        '    Green\n'
        '    Yellow\n'
        '    Blue\n'
        '    Magenta\n\n'
        '  Selected value: '
    )


def test_multi_select_example_first_frame_matches_snapshot():
    def Example():
        value, setValue = useState([])
        return Box(
            MultiSelect(options=OPTIONS, onChange=setValue),
            Text(f"Selected values: {', '.join(value)}"),
            flexDirection='column',
            padding=2,
            gap=1,
        )

    frame = _render_plain(Example)

    assert frame == (
        '\n\n'
        '  ❯ Red\n'
        '    Green\n'
        '    Yellow\n'
        '    Blue\n'
        '    Magenta\n\n'
        '  Selected values: '
    )


def test_spinner_status_and_input_examples_keep_current_first_frame_spacing():
    assert _render_plain(Box(createElement(Spinner, label='Loading'), padding=2)) == '\n\n  ⠋ Loading'
    assert _render_plain(
        Box(
            StatusMessage('Success', variant='success'),
            StatusMessage('Error', variant='error'),
            StatusMessage('Warning', variant='warning'),
            StatusMessage('Info', variant='info'),
            flexDirection='column',
            padding=2,
        )
    ) == '\n\n  ✔  Success\n  ✘  Error\n  ⚠  Warning\n  ℹ  Info'
    assert _render_plain(
        Box(
            TextInput(placeholder='Start typing...'),
            Text('Input value: ""'),
            flexDirection='column',
            padding=2,
            gap=1,
        )
    ) == '\n\n  Start typing...\n\n  Input value: ""'
    assert _render_plain(
        Box(
            EmailInput(placeholder='Enter email...'),
            Text('Input value: ""'),
            flexDirection='column',
            padding=2,
            gap=1,
        )
    ) == '\n\n  Enter email...\n\n  Input value: ""'
    assert _render_plain(
        Box(
            PasswordInput(placeholder='Enter password...'),
            Text('Input value: ""'),
            flexDirection='column',
            padding=2,
            gap=1,
        )
    ) == '\n\n  Enter password...\n\n  Input value: ""'
