# Password input

> `PasswordInput` is used for entering sensitive data, like passwords, API keys and so on. Input value is masked and replaced with asterisks ("*").

[Example code](../examples/password-input.py)

## Usage

```python
from pyinkui import PasswordInput, render


def App():
    return PasswordInput(placeholder='Enter password...')


if __name__ == '__main__':
    render(App).wait_until_exit()
```
