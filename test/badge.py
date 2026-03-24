import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pyinkcli import renderToString
from pyinkui import Badge
from tests.helpers import stripAnsi


def test_badge():
    output = renderToString(Badge('Success', color='green'))
    assert stripAnsi(output) == ' SUCCESS '
