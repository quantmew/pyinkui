import _bootstrap  # noqa: F401

from pyinkui import Alert, Box, render



def App():
    return Box(Alert('Message', variant='error', title='Error'), width=16)


if __name__ == '__main__':
    render(App).wait_until_exit()
