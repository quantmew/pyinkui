from __future__ import annotations

import fcntl
import os
from pathlib import Path
import pty
import select
import struct
import subprocess
import sys
import termios
import textwrap
import time
import re


ROOT = Path(__file__).resolve().parents[1]
CLI_ROOT = ROOT.parent / "pyinkcli"
ANSI_RE = re.compile(r"\x1b\[[0-9;?]*[A-Za-z]")


def _run_python_in_pty(
    source: str,
    *,
    send: bytes = b"",
    send_after_text: str | None = None,
    send_delay_after_text: float = 0.0,
    timeout: float = 3.0,
    rows: int | None = None,
    cols: int | None = None,
) -> str:
    master_fd, slave_fd = pty.openpty()
    if rows is not None or cols is not None:
        winsz = struct.pack("HHHH", rows or 24, cols or 80, 0, 0)
        fcntl.ioctl(slave_fd, termios.TIOCSWINSZ, winsz)

    env = os.environ.copy()
    env["PYTHONUNBUFFERED"] = "1"
    env["PYTHONPATH"] = f"{CLI_ROOT / 'src'}:{ROOT / 'src'}"

    process = subprocess.Popen(
        [sys.executable, "-c", source],
        stdin=slave_fd,
        stdout=slave_fd,
        stderr=slave_fd,
        close_fds=True,
        env=env,
        cwd=ROOT,
    )
    os.close(slave_fd)

    captured = bytearray()
    deadline = time.time() + timeout
    sent = False
    send_not_before: float | None = None

    try:
        while time.time() < deadline:
            if send and not sent and send_after_text is None:
                os.write(master_fd, send)
                sent = True

            if (
                send
                and not sent
                and send_not_before is not None
                and time.time() >= send_not_before
            ):
                os.write(master_fd, send)
                sent = True

            ready, _, _ = select.select([master_fd], [], [], 0.05)
            if master_fd in ready:
                try:
                    chunk = os.read(master_fd, 4096)
                except OSError:
                    break
                if not chunk:
                    break
                captured.extend(chunk)
                if (
                    send
                    and not sent
                    and send_after_text is not None
                    and send_after_text.encode() in captured
                    and send_not_before is None
                ):
                    send_not_before = time.time() + send_delay_after_text

            if process.poll() is not None:
                while True:
                    try:
                        chunk = os.read(master_fd, 4096)
                    except OSError:
                        break
                    if not chunk:
                        break
                    captured.extend(chunk)
                break
    finally:
        process.kill()
        process.wait(timeout=1)
        os.close(master_fd)

    return captured.decode("utf-8", errors="replace")


def _strip_ansi(value: str) -> str:
    return ANSI_RE.sub("", value)


def test_confirm_input_example_first_frame_in_real_tty() -> None:
    source = textwrap.dedent(
        f"""
        import runpy

        runpy.run_path({str(ROOT / "examples" / "confirm-input.py")!r}, run_name="__main__")
        """
    )
    output = _run_python_in_pty(
        source,
        send=b"\x03",
        send_after_text="Do you agree with terms of service? Y/n",
        send_delay_after_text=0.1,
        timeout=3.0,
        rows=20,
        cols=80,
    )

    assert "Do you agree with terms of service? Y/n" in _strip_ansi(output)


def test_select_example_first_frame_in_real_tty() -> None:
    source = textwrap.dedent(
        f"""
        import runpy

        runpy.run_path({str(ROOT / "examples" / "select" / "index.py")!r}, run_name="__main__")
        """
    )
    output = _run_python_in_pty(
        source,
        send=b"\x03",
        send_after_text="Selected value:",
        send_delay_after_text=0.1,
        timeout=3.0,
        rows=20,
        cols=80,
    )

    plain = _strip_ansi(output)
    assert "❯ Red" in plain
    assert "Selected value:" in plain
    assert "Selected value: None" not in plain


def test_text_input_example_first_frame_in_real_tty() -> None:
    source = textwrap.dedent(
        f"""
        import runpy

        runpy.run_path({str(ROOT / "examples" / "text-input.py")!r}, run_name="__main__")
        """
    )
    output = _run_python_in_pty(
        source,
        send=b"\x03",
        send_after_text="Input value:",
        send_delay_after_text=0.1,
        timeout=3.0,
        rows=20,
        cols=80,
    )

    plain = _strip_ansi(output)
    assert "Start typing..." in plain
    assert 'Input value: ""' in plain


def test_spinner_example_animates_in_real_tty() -> None:
    source = textwrap.dedent(
        f"""
        import runpy

        runpy.run_path({str(ROOT / "examples" / "spinner.py")!r}, run_name="__main__")
        """
    )
    output = _run_python_in_pty(
        source,
        send=b"\x03",
        send_after_text="Loading",
        send_delay_after_text=0.35,
        timeout=3.0,
        rows=20,
        cols=80,
    )

    plain = _strip_ansi(output)
    assert "⠋ Loading" in plain
    assert any(f"{frame} Loading" in plain for frame in ("⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"))
