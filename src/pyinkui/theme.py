from __future__ import annotations

from typing import Any

from pyinkui._merge import deepMerge
from pyinkui._theme_context import getThemeContext, provideThemeContext
from pyinkui._figures import info, tick, cross, warning, line, square, squareLightShade


badgeTheme = {
    'styles': {
        'container': lambda props=None: {'backgroundColor': (props or {}).get('color')},
        'label': lambda props=None: {'color': 'black'},
    }
}

confirmInputTheme = {
    'styles': {
        'input': lambda props=None: {'dimColor': not (props or {}).get('isFocused', False)},
    }
}

spinnerTheme = {
    'styles': {
        'container': lambda props=None: {'gap': 1},
        'frame': lambda props=None: {'color': 'blue'},
        'label': lambda props=None: {},
    }
}

textInputTheme: dict[str, Any] = {'styles': {'value': lambda props=None: {}}}
emailInputTheme: dict[str, Any] = {'styles': {'value': lambda props=None: {}}}
passwordInputTheme: dict[str, Any] = {'styles': {'value': lambda props=None: {}}}

selectTheme = {
    'styles': {
        'container': lambda props=None: {'flexDirection': 'column'},
        'option': lambda props=None: {'gap': 1, 'paddingLeft': 0 if (props or {}).get('isFocused') else 2},
        'selectedIndicator': lambda props=None: {'color': 'green'},
        'focusIndicator': lambda props=None: {'color': 'blue'},
        'label': lambda props=None: {
            'color': 'blue' if (props or {}).get('isFocused') else ('green' if (props or {}).get('isSelected') else None)
        },
        'highlightedText': lambda props=None: {'bold': True},
    },
}

multiSelectTheme = deepMerge(selectTheme, {})

orderedListTheme = {
    'styles': {
        'list': lambda props=None: {'flexDirection': 'column'},
        'listItem': lambda props=None: {'gap': 1},
        'marker': lambda props=None: {'dimColor': True},
        'content': lambda props=None: {'flexDirection': 'column'},
    }
}

unorderedListTheme = {
    'styles': {
        'list': lambda props=None: {'flexDirection': 'column'},
        'listItem': lambda props=None: {'gap': 1},
        'marker': lambda props=None: {'dimColor': True},
        'content': lambda props=None: {'flexDirection': 'column'},
    },
    'config': lambda props=None: {'marker': line},
}

progressBarTheme = {
    'styles': {
        'container': lambda props=None: {'flexGrow': 1, 'minWidth': 0},
        'completed': lambda props=None: {'color': 'magenta'},
        'remaining': lambda props=None: {'dimColor': True},
    },
    'config': lambda props=None: {
        'completedCharacter': square,
        'remainingCharacter': squareLightShade,
    },
}

statusMessageTheme = {
    'styles': {
        'container': lambda props=None: {'gap': 1},
        'iconContainer': lambda props=None: {'flexShrink': 0},
        'icon': lambda props=None: {'color': {'success': 'green', 'error': 'red', 'warning': 'yellow', 'info': 'blue'}[(props or {})['variant']]},
        'message': lambda props=None: {},
    },
    'config': lambda props=None: {
        'icon': {'success': tick, 'error': cross, 'warning': warning, 'info': info}[(props or {})['variant']]
    },
}

alertTheme = {
    'styles': {
        'container': lambda props=None: {
            'flexGrow': 1,
            'borderStyle': 'round',
            'borderColor': {'info': 'blue', 'success': 'green', 'error': 'red', 'warning': 'yellow'}[(props or {})['variant']],
            'gap': 1,
            'paddingX': 1,
        },
        'iconContainer': lambda props=None: {'flexShrink': 0},
        'icon': lambda props=None: {'color': {'info': 'blue', 'success': 'green', 'error': 'red', 'warning': 'yellow'}[(props or {})['variant']]},
        'content': lambda props=None: {'flexShrink': 1, 'flexGrow': 1, 'minWidth': 0, 'flexDirection': 'column', 'gap': 1},
        'title': lambda props=None: {'bold': True},
        'message': lambda props=None: {},
    },
    'config': lambda props=None: {
        'icon': {
            'info': info,
            'success': tick,
            'error': cross,
            'warning': warning,
        }[(props or {})['variant']]
    },
}


defaultTheme = {
    'components': {
        'Alert': alertTheme,
        'Badge': badgeTheme,
        'ConfirmInput': confirmInputTheme,
        'MultiSelect': multiSelectTheme,
        'OrderedList': orderedListTheme,
        'ProgressBar': progressBarTheme,
        'Select': selectTheme,
        'Spinner': spinnerTheme,
        'StatusMessage': statusMessageTheme,
        'UnorderedList': unorderedListTheme,
        'TextInput': textInputTheme,
        'EmailInput': emailInputTheme,
        'PasswordInput': passwordInputTheme,
    }
}


class ThemeContext:
    pass


def extendTheme(originalTheme: dict[str, Any], newTheme: dict[str, Any]) -> dict[str, Any]:
    return deepMerge(originalTheme, newTheme)


def ThemeProvider(*children, theme: dict[str, Any]):
    return provideThemeContext(*children, theme=theme)


def useComponentTheme(component: str):
    theme = getThemeContext() or defaultTheme
    return theme['components'][component]
