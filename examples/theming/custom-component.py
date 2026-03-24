from pyinkcli import Text, render
from pyinkcli.component import createElement
from pyinkui import ThemeProvider, defaultTheme, extendTheme, useComponentTheme


customLabelTheme = {
    'styles': {
        'label': lambda props=None: {'color': 'green'},
    }
}

customTheme = extendTheme(
    defaultTheme,
    {
        'components': {
            'CustomLabel': customLabelTheme,
        }
    },
)


def CustomLabel():
    styles = useComponentTheme('CustomLabel')['styles']
    return Text('Hello world', **styles['label']())


def App():
    return ThemeProvider(
        createElement(CustomLabel),
        theme=customTheme,
    )


if __name__ == '__main__':
    render(App, interactive=True).wait_until_exit()
