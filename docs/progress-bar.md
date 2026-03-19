# Progress bar

> `ProgressBar` is an extended version of [`Spinner`](spinner.md), where it's possible to calculate a progress percentage.

[Example code](../examples/progress-bar.py)

## Usage

```python
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
```

<img src="../media/progress-bar.gif" width="400">

## Props

### value

Type: `number` \
Minimum: `0` \
Maximum: `100` \
Default: `0`

Progress.
