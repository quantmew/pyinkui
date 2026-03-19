theme = {
    'styles': {
        'container': lambda props=None: {'backgroundColor': (props or {}).get('color')},
        'label': lambda props=None: {'color': 'black'},
    }
}

Theme = dict

__all__ = ['Theme', 'theme']
