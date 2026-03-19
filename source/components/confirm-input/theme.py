theme = {
    'styles': {
        'input': lambda props=None: {'dimColor': not (props or {}).get('isFocused', False)},
    }
}

Theme = dict

__all__ = ['Theme', 'theme']
