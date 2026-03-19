theme = {
    'styles': {
        'list': lambda props=None: {'flexDirection': 'column'},
        'listItem': lambda props=None: {'gap': 1},
        'marker': lambda props=None: {'dimColor': True},
        'content': lambda props=None: {'flexDirection': 'column'},
    }
}

Theme = dict

__all__ = ['Theme', 'theme']
