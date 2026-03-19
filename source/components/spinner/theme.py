theme = {
    'styles': {
        'container': lambda props=None: {'gap': 1},
        'frame': lambda props=None: {'color': 'blue'},
        'label': lambda props=None: {},
    }
}

Theme = dict

__all__ = ['Theme', 'theme']
