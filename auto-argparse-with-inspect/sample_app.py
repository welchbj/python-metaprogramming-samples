"""A simple demo automatically-created CLI."""

from framework import Application

app = Application()


@app.top_level
def top_level(*, verbose: bool = False):
    app.config['verbose'] = verbose


@app.cmd
def add(one: int, two: int):
    """Add two numbers."""
    result = one + two

    if app.config['verbose']:
        print(f'{one} + {two} = {result}')
    else:
        print(result)


@app.cmd
def sub(one: int, two: int):
    """Subtract two numbers."""
    result = one - two

    if app.config['verbose']:
        print(f'{one} - {two} = {result}')
    else:
        print(result)


@app.cmd
def invert(operand: int):
    result = ~operand

    if app.config['verbose']:
        print(f'~{bin(operand)} = {bin(result)}')
    else:
        print(bin(result))


if __name__ == '__main__':
    try:
        app.run()
    except ValueError as e:
        print(e)
