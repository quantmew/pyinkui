import time

from pyinkui import Spinner, spinners
from tests.helpers import RenderHarness


def test_spinner():
    harness = RenderHarness(Spinner(label='Loading'))
    try:
        frames = []
        spinner = spinners['dots']
        for _ in range(4):
            frames.append(harness.app._last_output)
            time.sleep(spinner['interval'] / 1000)
        assert len(set(frames)) > 1
    finally:
        harness.cleanup()
