from pyinkcli import renderToString
from pyinkui import StatusMessage


def test_error():
    output = renderToString(StatusMessage('Error', variant='error'))
    assert 'Error' in output
    assert '✖' in output
