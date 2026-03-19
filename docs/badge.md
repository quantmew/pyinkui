# Badge

> `Badge` can be used to indicate a status of a certain item, usually positioned nearby the element it's related to.

[Example code](../examples/badge.py)

## Usage

```python
from pyinkui import Badge, Box, render


def App():
    return Box(
        Badge('Pass', color='green'),
        Badge('Fail', color='red'),
        Badge('Warn', color='yellow'),
        Badge('Todo', color='blue'),
        gap=2,
    )


if __name__ == '__main__':
    render(App).wait_until_exit()
```

<img src="../media/badge.png" width="400">

## Props

### children

Type: `ReactNode`

Label.

### color

Type: [`TextProps['color']`](https://github.com/vadimdemedes/ink#color)

Color.
