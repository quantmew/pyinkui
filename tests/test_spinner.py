import time

from pyinkcli.component import createElement
from pyinkui import Spinner, spinners
from tests.helpers import RenderHarness


def test_spinner_cycles_frames():
    harness = RenderHarness(createElement(Spinner, label='Loading'))
    try:
        frames = []
        spinner = spinners['dots']
        for _ in range(4):
            harness.app.wait_until_render_flush(timeout=0.2)
            frames.append(harness.lastFrame())
            time.sleep(spinner['interval'] / 1000)
        assert len(set(frames)) > 1
    finally:
        harness.cleanup()
