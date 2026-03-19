import threading

from pyinkcli import Box, render
from pyinkui import ProgressBar
from pyinkcli.hooks import useEffect, useState



def App():
    progress, setProgress = useState(0)

    def effect():
        if progress == 100:
            return None

        timer = threading.Timer(0.05, lambda: setProgress(progress + 1))
        timer.daemon = True
        timer.start()

        def cleanup():
            timer.cancel()

        return cleanup

    useEffect(effect, (progress,))
    return Box(ProgressBar(value=progress), padding=2, width=30)


if __name__ == '__main__':
    render(App).wait_until_exit()
