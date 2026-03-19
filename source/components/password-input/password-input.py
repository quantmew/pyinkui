from pyinkcli import Text
from pyinkui.components.password_input import usePasswordInput, usePasswordInputState
from pyinkui.theme import useComponentTheme


def PasswordInput(*, isDisabled=False, placeholder='', onChange=None, onSubmit=None):
    state = usePasswordInputState(onChange=onChange, onSubmit=onSubmit)
    inputValue = usePasswordInput(
        isDisabled=isDisabled,
        placeholder=placeholder,
        state=state,
    )['inputValue']
    styles = useComponentTheme('PasswordInput')['styles']
    return Text(inputValue, **styles['value']())


__all__ = ['PasswordInput']
