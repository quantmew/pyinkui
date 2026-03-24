from pyinkui._pyinkcli_compat import should_enable_synchronized_output


def test_sync_output_disabled_for_vscode(monkeypatch):
    monkeypatch.delenv("PYINKUI_SYNC_OUTPUT", raising=False)
    monkeypatch.setenv("TERM_PROGRAM", "vscode")
    monkeypatch.delenv("TERM_PRODUCT", raising=False)
    assert should_enable_synchronized_output() is False


def test_sync_output_disabled_for_trae(monkeypatch):
    monkeypatch.delenv("PYINKUI_SYNC_OUTPUT", raising=False)
    monkeypatch.delenv("TERM_PROGRAM", raising=False)
    monkeypatch.setenv("TERM_PRODUCT", "Trae")
    assert should_enable_synchronized_output() is False


def test_sync_output_override_wins(monkeypatch):
    monkeypatch.setenv("PYINKUI_SYNC_OUTPUT", "1")
    monkeypatch.setenv("TERM_PROGRAM", "vscode")
    monkeypatch.setenv("TERM_PRODUCT", "Trae")
    assert should_enable_synchronized_output() is True
