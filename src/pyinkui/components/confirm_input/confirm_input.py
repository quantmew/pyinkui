from __future__ import annotations

from typing import Any, Callable, cast

from pyinkcli import Box, Text, useInput
from pyinkcli.component import createElement
from pyinkui.theme import useComponentTheme

useInput_ = cast(Any, useInput)


def _ConfirmInput(
    *,
    isDisabled: bool = False,
    defaultChoice: str = "confirm",
    submitOnEnter: bool = True,
    onConfirm: Callable[[], Any] | None = None,
    onCancel: Callable[[], Any] | None = None,
) -> Any:
    styles = useComponentTheme('ConfirmInput')['styles']

    def handleInput(input: str, key: Any) -> None:
        if isDisabled:
            return
        if input == 'y' or input == 'Y':
            if onConfirm:
                onConfirm()
            return
        if input == 'n' or input == 'N':
            if onCancel:
                onCancel()
            return
        if (key.return_pressed or input in ('\r', '\n')) and submitOnEnter:
            if defaultChoice == 'confirm':
                if onConfirm:
                    onConfirm()
            elif onCancel:
                onCancel()

    useInput_(handleInput)

    return Box(
        Text('Y/n' if defaultChoice == 'confirm' else 'y/N', **styles['input']({'isFocused': not isDisabled})),
    )


def ConfirmInput(
    *,
    isDisabled: bool = False,
    defaultChoice: str = "confirm",
    submitOnEnter: bool = True,
    onConfirm: Callable[[], Any] | None = None,
    onCancel: Callable[[], Any] | None = None,
) -> Any:
    return createElement(
        _ConfirmInput,
        isDisabled=isDisabled,
        defaultChoice=defaultChoice,
        submitOnEnter=submitOnEnter,
        onConfirm=onConfirm,
        onCancel=onCancel,
    )
