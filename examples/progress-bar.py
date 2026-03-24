import threading

from pyinkcli import Box, Text, render
from pyinkcli.hooks import useEffect, useState
from pyinkui import useComponentTheme


def InlineProgressBar(*, value, width):
    theme = useComponentTheme('ProgressBar')
    styles = theme['styles']
    config = theme['config']
    progress = min(100, max(0, value))
    complete = round((progress / 100) * width)
    remaining = width - complete
    children = []
    if complete > 0:
        children.append(Text(config()['completedCharacter'] * complete, **styles['completed']()))
    if remaining > 0:
        children.append(Text(config()['remainingCharacter'] * remaining, **styles['remaining']()))
    return Box(*children)


def Example():
    progress, setProgress = useState(0)

    def effect():
        if progress == 100:
            return

        timer = threading.Timer(0.05, lambda: setProgress(progress + 1))
        timer.daemon = True
        timer.start()

        def cleanup():
            timer.cancel()

        return cleanup

    useEffect(effect, (progress,))
    return Box(InlineProgressBar(value=progress, width=26), padding=2, width=30)


if __name__ == '__main__':
    render(Example, interactive=True).wait_until_exit()
