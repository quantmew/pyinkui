from pyinkcli import Box, render
from pyinkui import Spinner


def App():
    return Box(
        Spinner(label='Loading'),
        padding=2,
    )


if __name__ == '__main__':
    render(App, interactive=True).wait_until_exit()
