from pyinkcli import Text
from pyinkcli import render
from pyinkui import ThemeProvider, defaultTheme, extendTheme, use_component_theme


def custom_label():
    styles = use_component_theme('CustomLabel')
    return Text('Hello world', **styles['label']())


customTheme = extendTheme(
    defaultTheme,
    {
        'components': {
            'CustomLabel': {
                'styles': {
                    'label': lambda: {'color': 'green'},
                }
            }
        }
    },
)


def App():
    return ThemeProvider(custom_label(), theme=customTheme)


if __name__ == '__main__':
    render(App).wait_until_exit()
