from pyinkui._figures import cross, info, tick, warning

colorByVariant = {
    'info': 'blue',
    'success': 'green',
    'error': 'red',
    'warning': 'yellow',
}

theme = {
    'styles': {
        'container': lambda props=None: {
            'flexGrow': 1,
            'borderStyle': 'round',
            'borderColor': colorByVariant[(props or {})['variant']],
            'gap': 1,
            'paddingX': 1,
        },
        'iconContainer': lambda props=None: {'flexShrink': 0},
        'icon': lambda props=None: {'color': colorByVariant[(props or {})['variant']]},
        'content': lambda props=None: {
            'flexShrink': 1,
            'flexGrow': 1,
            'minWidth': 0,
            'flexDirection': 'column',
            'gap': 1,
        },
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

Theme = dict

__all__ = ['Theme', 'theme']
