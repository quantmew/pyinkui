from pyinkui import MultiSelect
from tests.helpers import RenderHarness


options = [
    {'label': 'Red', 'value': 'red'},
    {'label': 'Green', 'value': 'green'},
    {'label': 'Yellow', 'value': 'yellow'},
    {'label': 'Blue', 'value': 'blue'},
    {'label': 'Magenta', 'value': 'magenta'},
]


def test_toggle_focused_option():
    state = {'value': [], 'submitted': None}
    harness = RenderHarness(
        MultiSelect(
            options=options,
            onChange=lambda value: state.__setitem__('value', value),
            onSubmit=lambda value: state.__setitem__('submitted', value),
        )
    )
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
