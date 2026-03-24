from pyinkcli import Box, render
from pyinkui import Alert


def App():
    return Box(
        Alert('A new version of this CLI is available', variant='success'),
        Alert('Your license is expired', variant='error'),
        Alert('Current version of this CLI has been deprecated', variant='warning'),
        Alert("API won't be available tomorrow night", variant='info'),
        flexDirection='column',
        alignItems='stretch',
        padding=2,
        width=60,
        gap=1,
    )


if __name__ == '__main__':
    render(App, interactive=True).wait_until_exit()
