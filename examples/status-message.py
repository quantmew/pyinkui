import _bootstrap  # noqa: F401

from pyinkui import StatusMessage, render



def App():
    return StatusMessage('Ready', variant='success')


if __name__ == '__main__':
    render(App).wait_until_exit()
