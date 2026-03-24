from __future__ import annotations

import threading
from typing import Any, Callable, TypedDict, cast

from pyinkcli import Box, Text
from pyinkcli.hooks._runtime import useEffect, useState
from pyinkui.theme import useComponentTheme

useEffect_ = cast(Any, useEffect)
useState_ = cast(Any, useState)

class SpinnerConfig(TypedDict):
    interval: int
    frames: list[str]

spinners: dict[str, SpinnerConfig] = {
    'dots': {
        'interval': 80,
        'frames': ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'],
    }
}


def useSpinner(*, type: str = 'dots') -> dict[str, str]:
    frame, setFrame = useState_(0)
    spinner = spinners[type]

    def effect() -> Callable[[], None]:
        stopped = threading.Event()

        def run() -> None:
            while not stopped.wait(spinner['interval'] / 1000):
                def update(previousFrame: int) -> int:
                    isLastFrame = previousFrame == len(spinner['frames']) - 1
                    return 0 if isLastFrame else previousFrame + 1
                setFrame(update)

        thread = threading.Thread(target=run, daemon=True)
        thread.start()

        def cleanup() -> None:
            stopped.set()

        return cleanup

    useEffect_(effect, (type,))
    frames = spinner['frames']
    return {'frame': frames[frame] if frame < len(frames) else ''}


def Spinner(*, label: str | None = None, type: str = 'dots') -> Any:
    frame = useSpinner(type=type)['frame']
    styles = useComponentTheme('Spinner')['styles']
    children: list[Any] = [Text(frame, **styles['frame']())]
    if label:
        children.append(Text(label, **styles['label']()))
    return Box(*children, **styles['container']())
