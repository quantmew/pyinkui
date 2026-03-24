from pyinkcli import Box, Text
from pyinkcli.hooks import useState
from pyinkui import MultiSelect, Select
from tests.helpers import RenderHarness, stripAnsi

options = [
    {'label': 'Red', 'value': 'red'},
    {'label': 'Green', 'value': 'green'},
    {'label': 'Yellow', 'value': 'yellow'},
    {'label': 'Blue', 'value': 'blue'},
    {'label': 'Magenta', 'value': 'magenta'},
    {'label': 'Cyan', 'value': 'cyan'},
    {'label': 'White', 'value': 'white'},
]


def test_select_changes_value_on_enter():
    state = {'value': None}
    harness = RenderHarness(Select(options=options, onChange=lambda value: state.__setitem__('value', value)))
    try:
        harness.write('\r')
        assert state['value'] == 'red'
        harness.write('\x1b[B')
        harness.write('\r')
        assert state['value'] == 'green'
    finally:
        harness.cleanup()


def test_select_shows_default_selected_option():
    harness = RenderHarness(Select(options=options, defaultValue='green'))
    try:
        frame = stripAnsi(harness.lastFrame())
        assert '❯ Red' in frame
        assert 'Green ✔' in frame
    finally:
        harness.cleanup()


def test_select_limits_visible_options_and_scrolls_focus_window():
    harness = RenderHarness(Select(options=options, visibleOptionCount=3))
    try:
        assert stripAnsi(harness.lastFrame()) == '\n'.join([
            '❯ Red',
            '  Green',
            '  Yellow',
        ])
        for _ in range(6):
            harness.write('\x1b[B')
        assert stripAnsi(harness.lastFrame()) == '\n'.join([
            '  Magenta',
            '  Cyan',
            '❯ White',
        ])
        harness.write('\x1b[B')
        assert stripAnsi(harness.lastFrame()) == '\n'.join([
            '  Magenta',
            '  Cyan',
            '❯ White',
        ])
    finally:
        harness.cleanup()


def test_select_disabled_ignores_navigation_and_submit():
    state = {'value': None}
    harness = RenderHarness(Select(options=options, isDisabled=True, onChange=lambda value: state.__setitem__('value', value)))
    try:
        initial = stripAnsi(harness.lastFrame())
        harness.write('\x1b[B')
        harness.write('\r')
        assert stripAnsi(harness.app._rendered_output) == initial
        assert state['value'] is None
    finally:
        harness.cleanup()


def test_select_highlight_text_marks_matching_substrings():
    harness = RenderHarness(Select(options=options, highlightText='l'))
    try:
        frame = harness.lastFrame()
        assert '\x1b[1ml\x1b[22m' in frame
        assert 'Ye' in frame and 'ow' in frame
        assert 'B' in frame and 'ue' in frame
    finally:
        harness.cleanup()


def test_select_options_same_content_do_not_reset_focus_but_changed_options_do():
    stable_options = list(options)
    harness = RenderHarness(Select(options=stable_options))
    try:
        harness.write('\x1b[B')
        assert '❯ Green' in stripAnsi(harness.lastFrame())
        harness.rerender(Select(options=[dict(option) for option in stable_options]))
        assert '❯ Green' in stripAnsi(harness.app._rendered_output)
        changed_options = stable_options[1:]
        harness.rerender(Select(options=changed_options))
        frame = stripAnsi(harness.app._rendered_output)
        assert '❯ Green' in frame
        assert 'Red' not in frame
    finally:
        harness.cleanup()


def test_multi_select_toggle_and_submit():
    state = {'value': [], 'submitted': None}
    harness = RenderHarness(MultiSelect(options=options, onChange=lambda value: state.__setitem__('value', value), onSubmit=lambda value: state.__setitem__('submitted', value)))
    try:
        harness.write(' ')
        assert state['value'] == ['red']
        harness.write('\x1b[B')
        harness.write(' ')
        assert state['value'] == ['red', 'green']
        harness.write('\r')
        assert state['submitted'] == ['red', 'green']
    finally:
        harness.cleanup()


def test_multi_select_scrolls_and_toggle_is_reversible():
    state = {'value': []}
    harness = RenderHarness(MultiSelect(options=options, visibleOptionCount=3, onChange=lambda value: state.__setitem__('value', value)))
    try:
        assert stripAnsi(harness.lastFrame()) == '\n'.join([
            '❯ Red',
            '  Green',
            '  Yellow',
        ])
        harness.write('\x1b[B')
        harness.write(' ')
        assert state['value'] == ['green']
        harness.write(' ')
        assert state['value'] == []
        for _ in range(6):
            harness.write('\x1b[B')
        assert stripAnsi(harness.lastFrame()) == '\n'.join([
            '  Magenta',
            '  Cyan',
            '❯ White',
        ])
    finally:
        harness.cleanup()


def test_multi_select_disabled_ignores_input():
    state = {'value': [], 'submitted': None}
    harness = RenderHarness(
        MultiSelect(
            options=options,
            isDisabled=True,
            onChange=lambda value: state.__setitem__('value', value),
            onSubmit=lambda value: state.__setitem__('submitted', value),
        )
    )
    try:
        initial = stripAnsi(harness.lastFrame())
        harness.write('\x1b[B')
        harness.write(' ')
        harness.write('\r')
        assert stripAnsi(harness.app._rendered_output) == initial
        assert state['value'] == []
        assert state['submitted'] is None
    finally:
        harness.cleanup()


def test_multi_select_selected_options_by_default_and_submit_order():
    state = {'submitted': None}
    harness = RenderHarness(
        MultiSelect(
            options=options,
            defaultValue=['green', 'magenta'],
            onSubmit=lambda value: state.__setitem__('submitted', value),
        )
    )
    try:
        frame = stripAnsi(harness.lastFrame())
        assert '❯ Red' in frame
        assert 'Green ✔' in frame
        assert 'Magenta ✔' in frame
        harness.write('\r')
        assert state['submitted'] == ['green', 'magenta']
    finally:
        harness.cleanup()


def test_multi_select_highlight_text_marks_matching_substrings():
    harness = RenderHarness(MultiSelect(options=options, highlightText='l'))
    try:
        frame = harness.lastFrame()
        assert '\x1b[1ml\x1b[22m' in frame
        assert 'Ye' in frame and 'ow' in frame
        assert 'B' in frame and 'ue' in frame
    finally:
        harness.cleanup()


def test_multi_select_options_same_content_do_not_reset_focus_but_changed_options_do():
    stable_options = list(options)
    harness = RenderHarness(MultiSelect(options=stable_options))
    try:
        harness.write('\x1b[B')
        assert '❯ Green' in stripAnsi(harness.lastFrame())
        harness.rerender(MultiSelect(options=[dict(option) for option in stable_options]))
        assert '❯ Green' in stripAnsi(harness.app._rendered_output)
        changed_options = stable_options[1:]
        harness.rerender(MultiSelect(options=changed_options))
        frame = stripAnsi(harness.app._rendered_output)
        assert '❯ Green' in frame
        assert 'Red' not in frame
    finally:
        harness.cleanup()


def test_select_example_style_initial_value_is_blank_not_none():
    def Example():
        value, setValue = useState('')
        return Box(
            Select(options=options, onChange=setValue),
            Text(f'Selected value: {value}'),
            flexDirection='column',
            gap=1,
        )

    harness = RenderHarness(Example)
    try:
        frame = stripAnsi(harness.lastFrame())
        assert 'Selected value: None' not in frame
        assert 'Selected value: ' in frame
    finally:
        harness.cleanup()
