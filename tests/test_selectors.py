from pyinkui import MultiSelect, Select
from tests.helpers import RenderHarness

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
