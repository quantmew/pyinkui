from pyinkcli import Box, Text, render
from pyinkui import OrderedList


def App():
    return Box(
        OrderedList(
            OrderedList.Item(Text('Red')),
            OrderedList.Item(
                Text('Green'),
                OrderedList(
                    OrderedList.Item(Text('Light')),
                    OrderedList.Item(Text('Dark')),
                ),
            ),
            OrderedList.Item(Text('Blue')),
        ),
        padding=2,
    )


if __name__ == '__main__':
    render(App, interactive=True).wait_until_exit()
