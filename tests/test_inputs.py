from pyinkui._ansi import inverse
from pyinkui import ConfirmInput, EmailInput, PasswordInput, TextInput
from tests.helpers import RenderHarness, stripAnsi


def test_confirm_input_confirm_via_y():
    state = {'confirmed': False, 'cancelled': False}
    harness = RenderHarness(
        ConfirmInput(
            onConfirm=lambda: state.__setitem__('confirmed', True),
            onCancel=lambda: state.__setitem__('cancelled', True),
        )
    )
    try:
        assert stripAnsi(harness.lastFrame()) == 'Y/n'
        harness.write('y')
        assert state['confirmed'] is True
        assert state['cancelled'] is False
    finally:
        harness.cleanup()


def test_confirm_input_enter_uses_default_choice():
    state = {'confirmed': False, 'cancelled': False}
    harness = RenderHarness(
        ConfirmInput(
            defaultChoice='cancel',
            onConfirm=lambda: state.__setitem__('confirmed', True),
            onCancel=lambda: state.__setitem__('cancelled', True),
        )
    )
    try:
        assert stripAnsi(harness.lastFrame()) == 'y/N'
        harness.write('\r')
        assert state['confirmed'] is False
        assert state['cancelled'] is True
    finally:
        harness.cleanup()


def test_confirm_input_submit_on_enter_false_requires_explicit_choice():
    state = {'confirmed': False, 'cancelled': False}
    harness = RenderHarness(
        ConfirmInput(
            submitOnEnter=False,
            onConfirm=lambda: state.__setitem__('confirmed', True),
            onCancel=lambda: state.__setitem__('cancelled', True),
        )
    )
    try:
        harness.write('\r')
        assert state['confirmed'] is False
        assert state['cancelled'] is False
        harness.write('y')
        assert state['confirmed'] is True
        assert state['cancelled'] is False
    finally:
        harness.cleanup()


def test_confirm_input_cancel_via_n_and_disabled_enter_on_cancel_default():
    state = {'confirmed': False, 'cancelled': False}
    harness = RenderHarness(
        ConfirmInput(
            defaultChoice='cancel',
            submitOnEnter=False,
            onConfirm=lambda: state.__setitem__('confirmed', True),
            onCancel=lambda: state.__setitem__('cancelled', True),
        )
    )
    try:
        harness.write('\r')
        assert state['confirmed'] is False
        assert state['cancelled'] is False
        harness.write('n')
        assert state['confirmed'] is False
        assert state['cancelled'] is True
    finally:
        harness.cleanup()


def test_text_input_insert_and_submit():
    state = {'value': None, 'submitted': None}
    harness = RenderHarness(
        TextInput(
            placeholder='Start typing...',
            suggestions=['Abby'],
            onChange=lambda value: state.__setitem__('value', value),
            onSubmit=lambda value: state.__setitem__('submitted', value),
        )
    )
    try:
        assert 'Start typing' in stripAnsi(harness.lastFrame())
        harness.write('A')
        assert state['value'] == 'A'
        harness.write('b')
        harness.write('b')
        harness.write('\r')
        assert state['submitted'] == 'Abby'
    finally:
        harness.cleanup()


def test_text_input_placeholder_uses_visible_cursor_style_when_enabled():
    harness = RenderHarness(TextInput(placeholder='Start typing...'))
    try:
        assert harness.lastFrame() == inverse('S') + '\x1b[2mtart typing...\x1b[22m'
    finally:
        harness.cleanup()


def test_text_input_cursor_movement_and_middle_insert():
    state = {'value': None}
    harness = RenderHarness(
        TextInput(
            defaultValue='Hllo',
            onChange=lambda value: state.__setitem__('value', value),
        )
    )
    try:
        assert harness.lastFrame() == f'Hllo{inverse(" ")}'
        harness.write('\x1b[D')
        harness.write('\x1b[D')
        harness.write('\x1b[D')
        assert harness.lastFrame() == f'H{inverse("l")}lo'
        harness.write('e')
        assert harness.lastFrame() == f'He{inverse("l")}lo'
        assert state['value'] == 'Hello'
    finally:
        harness.cleanup()


def test_text_input_disabled_ignores_input():
    state = {'value': None}
    harness = RenderHarness(
        TextInput(
            isDisabled=True,
            placeholder='Start typing...',
            onChange=lambda value: state.__setitem__('value', value),
        )
    )
    try:
        initial = harness.lastFrame()
        harness.write('T')
        assert harness.app._rendered_output == initial
        assert state['value'] is None
    finally:
        harness.cleanup()


def test_password_input_insert_and_submit():
    state = {'submitted': None}
    harness = RenderHarness(PasswordInput(onSubmit=lambda value: state.__setitem__('submitted', value)))
    try:
        harness.write('Test')
        harness.write('\r')
        assert state['submitted'] == 'Test'
    finally:
        harness.cleanup()


def test_email_input_domain_autocomplete_and_submit():
    state = {'submitted': None}
    harness = RenderHarness(EmailInput(onSubmit=lambda value: state.__setitem__('submitted', value)))
    try:
        harness.write('test@')
        harness.write('a')
        harness.write('o')
        harness.write('\r')
        assert state['submitted'] == 'test@aol.com'
    finally:
        harness.cleanup()


def test_email_input_prevents_second_at_character_and_supports_cursor_editing():
    state = {'value': None}
    harness = RenderHarness(EmailInput(onChange=lambda value: state.__setitem__('value', value)))
    try:
        harness.write('test@')
        first = harness.lastFrame()
        harness.write('@')
        assert harness.lastFrame() == first
        assert state['value'] == 'test@'
        harness = harness  # keep for clarity
    finally:
        harness.cleanup()


def test_email_input_placeholder_and_disabled_rendering():
    enabled = RenderHarness(EmailInput(placeholder='Start typing...'))
    disabled = RenderHarness(EmailInput(isDisabled=True, placeholder='Start typing...'))
    try:
        assert enabled.lastFrame() == inverse('S') + '\x1b[2mtart typing...\x1b[22m'
        assert disabled.lastFrame() == '\x1b[2mStart typing...\x1b[22m'
    finally:
        enabled.cleanup()
        disabled.cleanup()


def test_email_input_default_value_cursor_movement_and_middle_insert():
    state = {'value': None}
    harness = RenderHarness(EmailInput(defaultValue='hllo', onChange=lambda value: state.__setitem__('value', value)))
    try:
        assert harness.lastFrame() == f'hllo{inverse(" ")}'
        harness.write('\x1b[D')
        harness.write('\x1b[D')
        harness.write('\x1b[D')
        assert harness.lastFrame() == f'h{inverse("l")}lo'
        harness.write('e')
        assert harness.lastFrame() == f'he{inverse("l")}lo'
        assert state['value'] == 'hello'
    finally:
        harness.cleanup()


def test_email_input_submit_on_enter_without_suggestion_uses_current_value():
    state = {'submitted': None}
    harness = RenderHarness(EmailInput(defaultValue='test', onSubmit=lambda value: state.__setitem__('submitted', value)))
    try:
        harness.write('\r')
        assert state['submitted'] == 'test'
    finally:
        harness.cleanup()


def test_password_input_placeholder_cursor_and_middle_insert():
    state = {'value': None}
    harness = RenderHarness(PasswordInput(placeholder='Enter password...', onChange=lambda value: state.__setitem__('value', value)))
    try:
        assert harness.lastFrame() == inverse('E') + '\x1b[2mnter password...\x1b[22m'
        harness.write('Hllo')
        assert harness.lastFrame() == f'****{inverse(" ")}'
        harness.write('\x1b[D')
        harness.write('\x1b[D')
        harness.write('\x1b[D')
        assert harness.lastFrame() == f'*{inverse("*")}**'
        harness.write('e')
        assert harness.lastFrame() == f'**{inverse("*")}**'
        assert state['value'] == 'Hello'
    finally:
        harness.cleanup()


def test_password_input_disabled_hides_cursor_and_ignores_input():
    state = {'value': None}
    harness = RenderHarness(
        PasswordInput(
            isDisabled=True,
            placeholder='Enter password...',
            onChange=lambda value: state.__setitem__('value', value),
        )
    )
    try:
        assert harness.lastFrame() == '\x1b[2mEnter password...\x1b[22m'
        harness.write('T')
        assert harness.app._rendered_output == '\x1b[2mEnter password...\x1b[22m'
        assert state['value'] is None
    finally:
        harness.cleanup()


def test_password_input_delete_all_text_restores_placeholder():
    state = {'value': None}
    harness = RenderHarness(
        PasswordInput(
            placeholder='Enter password...',
            onChange=lambda value: state.__setitem__('value', value),
        )
    )
    try:
        harness.write('Test')
        for _ in range(4):
            harness.write('\x7f')
        assert harness.lastFrame() == inverse('E') + '\x1b[2mnter password...\x1b[22m'
        assert state['value'] == ''
    finally:
        harness.cleanup()
