from pyinkui import Badge, renderToString
from tests.helpers import stripAnsi


def test_badge():
    output = renderToString(Badge('Success', color='green'))
    assert stripAnsi(output) == ' SUCCESS '
