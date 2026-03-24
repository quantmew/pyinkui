import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pyinkui import EmailInput
from tests.helpers import RenderHarness


def test_submit_on_enter():
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
