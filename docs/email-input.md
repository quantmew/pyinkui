# Email input

> `EmailInput` is used for entering an email. After "@" character is entered, domain can be autocompleted from the list of most popular email providers.

[Example code](../examples/email-input.py)

## Usage

```python
from pyinkcli import render
from pyinkui import EmailInput


def App():
    return EmailInput(placeholder='Enter email...')


if __name__ == '__main__':
    render(App).wait_until_exit()
```
