import _bootstrap  # noqa: F401

from pyinkui import Badge, render



def App():
    return Badge('Success', color='green')


if __name__ == '__main__':
    render(App).wait_until_exit()
