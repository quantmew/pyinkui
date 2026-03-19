from __future__ import annotations

import re
import time
from io import StringIO

from pyinkcli.hooks.use_input import _dispatch_input
from pyinkcli import render


class RenderHarness:
    def __init__(self, node):
        self.stdout = StringIO()
        self.stderr = StringIO()
        self.stdin = StringIO()
        self.app = render(
            node,
            stdout=self.stdout,
            stderr=self.stderr,
            stdin=self.stdin,
            interactive=False,
            debug=True,
            patch_console=False,
        )
        self.app.wait_until_render_flush(timeout=1.0)

    def clear(self):
        self.stdout.seek(0)
        self.stdout.truncate(0)

    def lastFrame(self) -> str:
        return self.stdout.getvalue()

    def write(self, data: str):
        self.clear()
        if data.startswith('\x1b') or len(data) <= 1:
            _dispatch_input(data)
        else:
            for character in data:
                _dispatch_input(character)
        self.app.wait_until_render_flush(timeout=1.0)

    def rerender(self, node):
        self.clear()
        self.app.rerender(node)
        self.app.wait_until_render_flush(timeout=1.0)

    def cleanup(self):
        self.app.unmount()


def wait(seconds: float):
    time.sleep(seconds)


_ansiPattern = re.compile(r'\x1b\[[0-9;?]*[A-Za-z]')


def stripAnsi(value: str) -> str:
    return _ansiPattern.sub('', value)
