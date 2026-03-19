import _bootstrap  # noqa: F401

from pyinkui import ThemeProvider, UnorderedList, Text, defaultTheme, extendTheme, render


customTheme = extendTheme(
    defaultTheme,
    {
        'components': {
            'UnorderedList': {
                'config': lambda props=None: {'marker': ['+', '*']},
            }
        }
    },
)


def App():
    return ThemeProvider(
        UnorderedList(
            UnorderedList.Item(Text('Red')),
            UnorderedList.Item(
                Text('Green'),
                UnorderedList(
                    UnorderedList.Item(Text('Light')),
                    UnorderedList.Item(Text('Dark')),
                ),
            ),
        ),
        theme=customTheme,
    )


if __name__ == '__main__':
    render(App).wait_until_exit()
