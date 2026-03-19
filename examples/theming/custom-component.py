import _bootstrap  # noqa: F401

from pyinkui import Badge, ThemeProvider, defaultTheme, extendTheme, render


customTheme = extendTheme(
    defaultTheme,
    {
        'components': {
            'Badge': {
                'styles': {
                    'container': lambda props=None: {'backgroundColor': 'cyan'},
                    'label': lambda props=None: {'color': 'black', 'bold': True},
                }
            }
        }
    },
)


def App():
    return ThemeProvider(Badge('custom'), theme=customTheme)


if __name__ == '__main__':
    render(App).wait_until_exit()
