import _bootstrap  # noqa: F401

from pyinkui import TextInput, render


def App():
    return TextInput(placeholder='Start typing...', suggestions=['Abby', 'Ada', 'Aiko'])


if __name__ == '__main__':
    render(App).wait_until_exit()
