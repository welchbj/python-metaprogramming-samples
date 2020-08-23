# Network Import Loader

This code demonstrates the basics of hooking the import system, and (ab)using it to load a module over a TCP connection.

## Example Usage

```sh
# Let the server run.
$ python server.py

# Trigger the import
$ python client.py
Successfully imported!
```