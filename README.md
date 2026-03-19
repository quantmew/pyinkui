# pyinkui

`pyinkui` is a Python translation of [`@inkjs/ui`](https://github.com/vadimdemedes/ink-ui), built on top of the already-translated [`pyinkcli`](https://github.com/quantmew/pyinkcli) runtime.

## Installation

`pyproject.toml` installs `pyinkcli` directly from:

- `https://github.com/quantmew/pyinkcli.git`

```bash
pip install -e .
```

If you want to install the runtime explicitly first:

```bash
pip install "pyinkcli @ git+https://github.com/quantmew/pyinkcli.git"
pip install -e .
```

## Quick Start

```python
from pyinkui import Box, Spinner, StatusMessage, render


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

## License

MIT. The license text is copied from upstream `ink-ui`.
