from pyinkcli import Box, Text, render
from pyinkui import Select, TextInput
from pyinkcli.hooks import useMemo, useState


def App():
    filter_text, set_filter_text = useState('')
    value, setValue = useState(None)

    options = useMemo(
        lambda: [
            {'label': 'Red', 'value': 'red'},
            {'label': 'Green', 'value': 'green'},
            {'label': 'Yellow', 'value': 'yellow'},
            {'label': 'Blue', 'value': 'blue'},
            {'label': 'Magenta', 'value': 'magenta'},
            {'label': 'Cyan', 'value': 'cyan'},
            {'label': 'White', 'value': 'white'},
        ],
        [],
    )

    filtered_options = [
        option for option in options if filter_text in option['label']
    ]

    if value is None:
        return Box(
            TextInput(onChange=set_filter_text),
            Select(
                options=filtered_options,
                highlightText=filter_text,
                onChange=setValue,
                visibleOptionCount=5,
            ),
            flexDirection='column',
            gap=1,
        )
    else:
        return Text(f"You've selected {value}")


if __name__ == '__main__':
    render(App, interactive=True).wait_until_exit()
