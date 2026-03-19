from pyinkui import OrderedList, Text, renderToString


def test_ordered_list():
    output = renderToString(
        OrderedList(
            OrderedList.Item(Text('Red')),
            OrderedList.Item(Text('Green')),
            OrderedList.Item(Text('Yellow')),
        ),
        columns=40,
        rows=10,
    )
    assert '1.' in output and '2.' in output and '3.' in output
