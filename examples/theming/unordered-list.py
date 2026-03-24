from pyinkcli import Box, Text, render
from pyinkui import ThemeProvider, UnorderedList, defaultTheme, extendTheme


customTheme = extendTheme(
    defaultTheme,
    {
        'components': {
            'UnorderedList': {
                'config': lambda: {'marker': '+'},
            }
        }
    },
)


def App():
    return ThemeProvider(
        Box(
            UnorderedList(
                UnorderedList.Item(Text('Red')),
                UnorderedList.Item(
                    Text('Green'),
                    UnorderedList(
                        UnorderedList.Item(Text('Light')),
                        UnorderedList.Item(Text('Dark')),
                    ),
                ),
                UnorderedList.Item(Text('Blue')),
            ),
            padding=2,
        ),
        theme=customTheme,
    )


if __name__ == '__main__':
    render(App, interactive=True).wait_until_exit()
