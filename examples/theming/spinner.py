import _bootstrap  # noqa: F401

from pyinkui import Spinner, ThemeProvider, defaultTheme, extendTheme, render


customTheme = extendTheme(
    defaultTheme,
    {
        'components': {
            'Spinner': {
                'styles': {
                    'frame': lambda props=None: {'color': 'green'},
                }
            }
        }
    },
)


def App():
    return ThemeProvider(Spinner(label='Loading'), theme=customTheme)


if __name__ == '__main__':
    render(App).wait_until_exit()
