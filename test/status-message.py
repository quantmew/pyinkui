from pyinkui import StatusMessage, renderToString


def test_error():
    output = renderToString(StatusMessage('Error', variant='error'))
    assert 'Error' in output
    assert '✖' in output
