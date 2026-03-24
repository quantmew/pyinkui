import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pyinkcli import Box
from pyinkui import ProgressBar
from tests.helpers import RenderHarness, stripAnsi


def test_progress_bar():
    harness = RenderHarness(Box(ProgressBar(value=50), width=20))
    try:
        assert stripAnsi(harness.lastFrame()) == '██████████░░░░░░░░░░'
    finally:
        harness.cleanup()
