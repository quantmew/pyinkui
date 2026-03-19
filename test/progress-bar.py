from pyinkui import Box, ProgressBar
from tests.helpers import RenderHarness


def test_progress_bar():
    harness = RenderHarness(Box(ProgressBar(value=50), width=20))
    try:
        assert harness.lastFrame() != ''
    finally:
        harness.cleanup()
