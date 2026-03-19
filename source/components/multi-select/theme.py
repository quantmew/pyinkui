theme = {
    'styles': {
        'container': lambda props=None: {'flexDirection': 'column'},
        'option': lambda props=None: {'gap': 1, 'paddingLeft': 0 if (props or {}).get('isFocused') else 2},
        'selectedIndicator': lambda props=None: {'color': 'green'},
        'focusIndicator': lambda props=None: {'color': 'blue'},
        'label': lambda props=None: {
            'color': 'blue' if (props or {}).get('isFocused') else ('green' if (props or {}).get('isSelected') else None)
        },
        'highlightedText': lambda props=None: {'bold': True},
    }
}

Theme = dict

__all__ = ['Theme', 'theme']
