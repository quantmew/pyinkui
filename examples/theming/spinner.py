from pyinkcli import Box, Text
from pyinkcli import render
from pyinkui import Spinner, ThemeProvider, defaultTheme, extendTheme


customTheme = extendTheme(
    defaultTheme,
    {
        'components': {
            'Spinner': {
                'styles': {
                    'frame': lambda: {'color': 'magenta'},
                }
            }
        }
    },
)


def App():
    return ThemeProvider(
        Box(
            Spinner(label='Loading'),
            padding=2,
        ),
        theme=customTheme,
    )


if __name__ == '__main__':
    render(App).wait_until_exit()
