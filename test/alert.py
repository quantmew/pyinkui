from pyinkcli import Box, renderToString
from pyinkui import Alert


def test_error():
    output = renderToString(Box(Alert('Message', variant='error', title='Error'), width=16), columns=20, rows=10)
    assert 'Error' in output
    assert 'Message' in output
