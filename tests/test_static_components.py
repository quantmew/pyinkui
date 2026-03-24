from pyinkcli import Box, Text, renderToString
from pyinkcli.component import createElement
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
    useComponentTheme,
)
from tests.helpers import RenderHarness, stripAnsi


def test_badge():
    output = renderToString(Badge('Success', color='green'))
    assert stripAnsi(output) == ' SUCCESS '


def test_status_message_error():
    output = renderToString(StatusMessage('Error', variant='error'))
    assert 'Error' in output
    assert '✘' in output


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


def test_ordered_list_nested_markers_preserve_parent_prefix():
    output = renderToString(
        OrderedList(
            OrderedList.Item(Text('Red')),
            OrderedList.Item(
                Text('Green'),
                OrderedList(
                    OrderedList.Item(Text('Light')),
                    OrderedList.Item(Text('Dark')),
                ),
            ),
            OrderedList.Item(Text('Blue')),
        ),
        columns=40,
        rows=10,
    )

    assert '2.1.' in output
    assert '2.2.' in output


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


def test_unordered_list_custom_marker_propagates_to_nested_lists():
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
                UnorderedList.Item(
                    Text('Green'),
                    UnorderedList(
                        UnorderedList.Item(Text('Light')),
                        UnorderedList.Item(Text('Dark')),
                    ),
                ),
            ),
            theme=customTheme,
        ),
        columns=40,
        rows=10,
    )
    assert output.count('+') >= 4


def test_custom_component_can_read_extended_theme_section():
    customTheme = extendTheme(defaultTheme, {
        'components': {
            'CustomLabel': {
                'styles': {
                    'label': lambda props=None: {'color': 'green'},
                }
            }
        }
    })

    def CustomLabel():
        styles = useComponentTheme('CustomLabel')['styles']
        return Text('Hello world', **styles['label']())

    output = renderToString(
        ThemeProvider(
            createElement(CustomLabel),
            theme=customTheme,
        )
    )

    assert stripAnsi(output) == 'Hello world'
    assert '\x1b[32m' in output


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


def test_progress_bar_without_measured_width_renders_nothing():
    output = renderToString(ProgressBar(value=50))
    assert stripAnsi(output) == ''


def test_alert_warning_uses_warning_color_and_icon():
    output = renderToString(Box(Alert('Deprecated', variant='warning'), width=24), columns=30, rows=10)
    assert '⚠' in output
    assert '\x1b[33m' in output
