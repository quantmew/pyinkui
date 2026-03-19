from pyinkcli import Text, renderToString
from pyinkui import ThemeProvider, UnorderedList, defaultTheme, extendTheme


def test_custom_marker():
    customTheme = extendTheme(
        defaultTheme,
        {
            'components': {
                'UnorderedList': {
                    'config': lambda props=None: {'marker': '+'},
                }
            }
        },
    )
    output = renderToString(
        ThemeProvider(
            UnorderedList(
                UnorderedList.Item(Text('Red')),
                UnorderedList.Item(Text('Green')),
            ),
            theme=customTheme,
        ),
        columns=40,
        rows=10,
    )
    assert '+' in output
