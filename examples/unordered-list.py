import _bootstrap  # noqa: F401

from pyinkui import UnorderedList, Text, render



def App():
    return UnorderedList(
        UnorderedList.Item(Text('Red')),
        UnorderedList.Item(Text('Green')),
        UnorderedList.Item(Text('Blue')),
    )


if __name__ == '__main__':
    render(App).wait_until_exit()
