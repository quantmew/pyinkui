from __future__ import annotations

import threading

from pyinkcli.hooks._runtime import useEffect, useState

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
