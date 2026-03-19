from pyinkcli import Text
from pyinkui.components.email_input import useEmailInput, useEmailInputState
from pyinkui.theme import useComponentTheme


def EmailInput(
    *,
    isDisabled=False,
    defaultValue=None,
    placeholder='',
    domains=None,
    onChange=None,
    onSubmit=None,
):
    state = useEmailInputState(
        defaultValue=defaultValue or '',
        domains=domains,
        onChange=onChange,
        onSubmit=onSubmit,
    )
    inputValue = useEmailInput(
        isDisabled=isDisabled,
        placeholder=placeholder,
        state=state,
    )['inputValue']
    styles = useComponentTheme('EmailInput')['styles']
    return Text(inputValue, **styles['value']())


__all__ = ['EmailInput']
