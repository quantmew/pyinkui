import _bootstrap  # noqa: F401

from pyinkui import PasswordInput, render



def App():
    return PasswordInput(placeholder='Enter password...')


if __name__ == '__main__':
    render(App).wait_until_exit()
