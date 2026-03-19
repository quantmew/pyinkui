from pyinkcli import Box, Text, render
from pyinkui import UnorderedList


def App():
    return Box(
        UnorderedList(
            UnorderedList.Item(Text('Red')),
            UnorderedList.Item(
                Text('Green'),
                UnorderedList(
                    UnorderedList.Item(Text('Light')),
                    UnorderedList.Item(Text('Dark')),
                ),
            ),
            UnorderedList.Item(Text('Blue')),
        ),
        padding=2,
    )


if __name__ == '__main__':
    render(App).wait_until_exit()
