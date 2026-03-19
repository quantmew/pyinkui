from pyinkcli import Box, Text, renderToString
from pyinkui import (
    Alert,
    Badge,
    OrderedList,
    ProgressBar,
    StatusMessage,
    ThemeProvider,
    UnorderedList,
    defaultTheme,
    extendTheme,
)
from tests.helpers import RenderHarness, stripAnsi


def test_badge():
    output = renderToString(Badge('Success', color='green'))
    assert stripAnsi(output) == ' SUCCESS '


def test_status_message_error():
    output = renderToString(StatusMessage('Error', variant='error'))
    assert 'Error' in output
    assert '✖' in output


def test_alert_error():
    output = renderToString(Box(Alert('Message', variant='error', title='Error'), width=16), columns=20, rows=10)
    assert 'Error' in output
    assert 'Message' in output


def test_ordered_list():
    output = renderToString(
        OrderedList(
            OrderedList.Item(Text('Red')),
            OrderedList.Item(Text('Green')),
            OrderedList.Item(Text('Yellow')),
        ),
        columns=40,
        rows=10,
    )
    assert '1.' in output and '2.' in output and '3.' in output


def test_unordered_list_custom_marker():
    customTheme = extendTheme(defaultTheme, {
        'components': {
            'UnorderedList': {
                'config': lambda props=None: {'marker': '+'},
            }
        }
    })
    output = renderToString(
        ThemeProvider(
            UnorderedList(
                UnorderedList.Item(Text('Red')),
                UnorderedList.Item(Text('Green')),
            ),
            theme=customTheme,
        ),
        columns=40,
        rows=10,
    )
    assert '+' in output


def test_progress_bar_rerender_width():
    harness = RenderHarness(Box(ProgressBar(value=50), width=20))
    try:
        assert stripAnsi(harness.lastFrame()) == '██████████░░░░░░░░░░'
        harness.rerender(Box(ProgressBar(value=75), width=20))
        assert stripAnsi(harness.lastFrame()) == '███████████████░░░░░'
    finally:
        harness.cleanup()


def test_progress_bar_initial_width_renders_remaining_track():
    harness = RenderHarness(Box(ProgressBar(value=50), width=20))
    try:
        harness.rerender(Box(ProgressBar(value=0), width=20))
        assert stripAnsi(harness.lastFrame()) == '░░░░░░░░░░░░░░░░░░░░'
    finally:
        harness.cleanup()
