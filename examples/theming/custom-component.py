# This example demonstrates extending the theme.
#
# Note: Creating fully custom components in Python requires careful handling
# due to the difference between React JSX (deferred execution) and Python
# function calls (immediate execution).
#
# This example shows customizing an existing component (Spinner) instead.

from pyinkcli import Box, render
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
