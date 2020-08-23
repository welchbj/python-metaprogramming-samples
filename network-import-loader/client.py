"""Network module loader demo.

Based on code from the following sources:

https://dev.to/dangerontheranger/dependency-injection-with-import-hooks-in-python-3-5hap
https://github.com/python/cpython/blob/3.8/Lib/importlib/abc.py
https://docs.python.org/3/reference/import.html#finders-and-loaders

DISCLAIMER: This is wildly insecure.

"""

import importlib.abc
import importlib.machinery
import socket
import sys


class NetworkModuleImporter(importlib.abc.MetaPathFinder, importlib.abc.InspectLoader):
    """Lets the import machinery know if our loader should handle this import."""

    def find_spec(self, fullname, path, target):
        if fullname.startswith('__network'):
            return importlib.machinery.ModuleSpec(fullname, self)

    def is_package(self, fullname):
        return False

    def get_source(self, fullname):
        tokens = fullname.split('_')

        ip = '.'.join(tokens[3:7])
        port = int(tokens[7])

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, port))
        source = s.recv(0x1000).decode()
        return source


if __name__ == '__main__':
    sys.meta_path.append(NetworkModuleImporter())

    import __network_127_0_0_1_12345__ as hosted_module
    hosted_module.say_hi()
