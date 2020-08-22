# Auto-`argparse` Framework

This toy framework and sample application demonstrate how to use the [`inspect`](https://docs.python.org/3/library/inspect.html) module to remove the [`arparse`](https://docs.python.org/3/library/argparse.html)-to-function translation layer present in a lot of Python command-line programs.

Nothing in this repository is production ready. For a proven framework that achieves something similar (read: better) than the code here, check out the [Click project](https://click.palletsprojects.com).

## Example Usage

```sh
$ python sample_app.py sub --one 100 --two 101
-1

$ python sample_app.py --verbose add --one 100 --two 101
100 + 101 = 201
```