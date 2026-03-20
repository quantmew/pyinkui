# pyinkui

`pyinkui` is a Python translation of [`@inkjs/ui`](https://github.com/vadimdemedes/ink-ui), built on top of the already-translated [`pyinkcli`](https://github.com/quantmew/pyinkcli) runtime.

## Installation

`pyproject.toml` installs `pyinkcli` directly from:

- `https://github.com/quantmew/pyinkcli.git`

```bash
pip install -e .
```

## Quick Start

```python
from pyinkcli import Box, render
from pyinkui import Spinner, StatusMessage


def App():
    return Box(
        Spinner(label="Loading"),
        StatusMessage("Ready", variant="success"),
        flexDirection="column",
    )


render(App).wait_until_exit()
```

## Testing

```bash
PYTHONPATH=src pytest
```

## Examples

Examples are optimized to be directly runnable with Python. They keep the upstream-facing filenames where practical, and use a small bootstrap helper to ensure the local `src/` tree is imported correctly.

## License

MIT. The license text is copied from upstream `ink-ui`.
