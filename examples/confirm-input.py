from pyinkcli import Box, Text, render
from pyinkui import ConfirmInput
from pyinkcli.hooks import useState


def App():
    choice, set_choice = useState(None)

    if choice is None:
        return Box(
            Text('Do you agree with terms of service?', bold=True),
            ConfirmInput(
                onConfirm=lambda: set_choice('agreed'),
                onCancel=lambda: set_choice('disagreed'),
            ),
            gap=1,
        )
    elif choice == 'agreed':
        return Text("I know you haven't read them, but ok")
    else:
        return Text('Ok, whatever')


if __name__ == '__main__':
    render(App, interactive=True).wait_until_exit()
