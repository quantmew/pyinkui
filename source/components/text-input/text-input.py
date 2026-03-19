from pyinkcli import Text
from pyinkui.components.text_input import useTextInput, useTextInputState
from pyinkui.theme import useComponentTheme


def TextInput(
    *,
    isDisabled=False,
    defaultValue=None,
    placeholder='',
    suggestions=None,
    onChange=None,
    onSubmit=None,
):
    state = useTextInputState(
        defaultValue=defaultValue or '',
        suggestions=suggestions,
        onChange=onChange,
        onSubmit=onSubmit,
    )
    inputValue = useTextInput(
        isDisabled=isDisabled,
        placeholder=placeholder,
        state=state,
    )['inputValue']
    styles = useComponentTheme('TextInput')['styles']
    return Text(inputValue, **styles['value']())


__all__ = ['TextInput']
