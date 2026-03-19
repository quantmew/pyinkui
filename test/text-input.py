from pyinkui import TextInput
from tests.helpers import RenderHarness, stripAnsi


def test_submit_on_enter():
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
        harness.write('b')
        harness.write('b')
        harness.write('\r')
        assert state['submitted'] == 'Abby'
    finally:
        harness.cleanup()
