from pyinkui._figures import cross, info, tick, warning

colorByVariant = {
    'success': 'green',
    'error': 'red',
    'warning': 'yellow',
    'info': 'blue',
}

iconByVariant = {
    'success': tick,
    'error': cross,
    'warning': warning,
    'info': info,
}

theme = {
    'styles': {
        'container': lambda props=None: {'gap': 1},
        'iconContainer': lambda props=None: {'flexShrink': 0},
        'icon': lambda props=None: {'color': colorByVariant[(props or {})['variant']]},
        'message': lambda props=None: {},
    },
    'config': lambda props=None: {'icon': iconByVariant[(props or {})['variant']]},
}

Theme = dict

__all__ = ['Theme', 'theme']
