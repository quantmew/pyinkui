import _bootstrap  # noqa: F401

from pyinkui import EmailInput, render



def App():
    return EmailInput(placeholder='Enter email...')


if __name__ == '__main__':
    render(App).wait_until_exit()
