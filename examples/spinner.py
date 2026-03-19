import _bootstrap  # noqa: F401

from pyinkui import Spinner, render



def App():
    return Spinner(label='Loading')


if __name__ == '__main__':
    render(App).wait_until_exit()
