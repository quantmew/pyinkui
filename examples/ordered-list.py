import _bootstrap  # noqa: F401

from pyinkui import OrderedList, Text, render



def App():
    return OrderedList(
        OrderedList.Item(Text('Red')),
        OrderedList.Item(Text('Green')),
        OrderedList.Item(Text('Blue')),
    )


if __name__ == '__main__':
    render(App).wait_until_exit()
