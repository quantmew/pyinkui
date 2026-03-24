from __future__ import annotations

import os


def _env_flag(name: str) -> bool | None:
    value = os.getenv(name)
    if value is None:
        return None
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    return None


def should_enable_synchronized_output() -> bool:
    override = _env_flag("PYINKUI_SYNC_OUTPUT")
    if override is not None:
        return override

    term_program = os.getenv("TERM_PROGRAM", "").strip().lower()
    term_product = os.getenv("TERM_PRODUCT", "").strip().lower()

    # VS Code-style integrated terminals expose xterm.js-compatible env vars
    # but do not reliably present pyinkcli's synchronized-update escape
    # sequences as live redraws.
    unsupported = {"vscode", "trae"}
    if term_program in unsupported or term_product in unsupported:
        return False

    return True


def patch_pyinkcli_terminal_compat() -> None:
    if should_enable_synchronized_output():
        return

    try:
        import pyinkcli.runtime.output_driver as output_driver  # type: ignore[import-not-found]
        import pyinkcli.write_synchronized as write_synchronized
    except Exception:  # noqa: BLE001
        return

    def _disabled_should_synchronize(stream: object, interactive: bool | None = None) -> bool:
        return False

    write_synchronized.shouldSynchronize = _disabled_should_synchronize
    output_driver.shouldSynchronize = _disabled_should_synchronize


__all__ = ["patch_pyinkcli_terminal_compat", "should_enable_synchronized_output"]
