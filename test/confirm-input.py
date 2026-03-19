from pyinkui import ConfirmInput
from tests.helpers import RenderHarness


def test_confirm_via_y():
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
