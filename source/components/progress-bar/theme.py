from pyinkui._figures import square, squareLightShade

theme = {
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

Theme = dict

__all__ = ['Theme', 'theme']
