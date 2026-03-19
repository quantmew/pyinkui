from pyinkui import Select
from tests.helpers import RenderHarness


options = [
    {'label': 'Red', 'value': 'red'},
    {'label': 'Green', 'value': 'green'},
    {'label': 'Yellow', 'value': 'yellow'},
    {'label': 'Blue', 'value': 'blue'},
    {'label': 'Magenta', 'value': 'magenta'},
]


def test_select_focused_option():
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
