import _bootstrap  # noqa: F401

from pyinkui import Select, render

options = [
    {'label': 'Red', 'value': 'red'},
    {'label': 'Green', 'value': 'green'},
    {'label': 'Blue', 'value': 'blue'},
]



def App():
    return Select(options=options)


if __name__ == '__main__':
    render(App).wait_until_exit()
