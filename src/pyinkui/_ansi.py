from pyinkcli.colorize import colorize


def dim(text: str) -> str:
    return f"[2m{text}[22m"


def bold(text: str) -> str:
    return f"[1m{text}[22m"


def inverse(text: str) -> str:
    return f"[7m{text}[27m"


def color(text: str, value: str) -> str:
    return colorize(text, value, 'foreground')


def background(text: str, value: str) -> str:
    return colorize(text, value, 'background')
