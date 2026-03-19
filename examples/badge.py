from pyinkcli import Box, render
from pyinkui import Badge


def App():
    return Box(
        Badge('Pass', color='green'),
        Badge('Fail', color='red'),
        Badge('Warn', color='yellow'),
        Badge('Todo', color='blue'),
        gap=2,
        padding=2,
    )


if __name__ == '__main__':
    render(App).wait_until_exit()
