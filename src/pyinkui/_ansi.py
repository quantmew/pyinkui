ANSI_FOREGROUND = {
    'black': 30,
    'red': 31,
    'green': 32,
    'yellow': 33,
    'blue': 34,
    'magenta': 35,
    'cyan': 36,
    'white': 37,
    'gray': 90,
    'grey': 90,
}

ANSI_BACKGROUND = {
    name: code + 10 for name, code in ANSI_FOREGROUND.items() if code < 90
}
ANSI_BACKGROUND['gray'] = 100
ANSI_BACKGROUND['grey'] = 100


def dim(text: str) -> str:
    return f"[2m{text}[22m"


def bold(text: str) -> str:
    return f"[1m{text}[22m"


def inverse(text: str) -> str:
    return f"[7m{text}[27m"


def color(text: str, value: str) -> str:
    code = ANSI_FOREGROUND.get(value)
    return text if code is None else f"\x1b[{code}m{text}\x1b[39m"


def background(text: str, value: str) -> str:
    code = ANSI_BACKGROUND.get(value)
    return text if code is None else f"\x1b[{code}m{text}\x1b[49m"
