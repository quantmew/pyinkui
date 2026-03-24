import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pyinkui import PasswordInput
from tests.helpers import RenderHarness


def test_submit_on_enter():
    state = {'submitted': None}
    harness = RenderHarness(PasswordInput(onSubmit=lambda value: state.__setitem__('submitted', value)))
    try:
        harness.write('Test')
        harness.write('\r')
        assert state['submitted'] == 'Test'
    finally:
        harness.cleanup()
