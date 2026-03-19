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
        assert harness.lastFrame() == 'Y/n'
        harness.write('y')
        assert state['confirmed'] is True
        assert state['cancelled'] is False
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
