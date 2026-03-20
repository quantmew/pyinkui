from __future__ import annotations

import threading

from pyinkcli import Box, Text
from pyinkcli.component import createElement
from pyinkcli.hooks._runtime import useEffect, useState
from pyinkui.theme import useComponentTheme

spinners = {
    'dots': {
        'interval': 80,
        'frames': ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'],
    }
}


def useSpinner(*, type='dots'):
    frame, setFrame = useState(0)
    spinner = spinners[type]

    def effect():
        stopped = threading.Event()

        def run():
            while not stopped.wait(spinner['interval'] / 1000):
                def update(previousFrame):
                    isLastFrame = previousFrame == len(spinner['frames']) - 1
                    return 0 if isLastFrame else previousFrame + 1
                setFrame(update)

        thread = threading.Thread(target=run, daemon=True)
        thread.start()

        def cleanup():
            stopped.set()

        return cleanup

    useEffect(effect, (type,))
    return {'frame': spinner['frames'][frame] if frame < len(spinner['frames']) else ''}


def _Spinner(*, label=None, spinnerType='dots'):
    frame = useSpinner(type=spinnerType)['frame']
    styles = useComponentTheme('Spinner')['styles']
    children = [Text(frame, **styles['frame']())]
    if label:
        children.append(Text(label, **styles['label']()))
    return Box(*children, **styles['container']())


def Spinner(*, label=None, type='dots'):
    return createElement(_Spinner, label=label, spinnerType=type)
