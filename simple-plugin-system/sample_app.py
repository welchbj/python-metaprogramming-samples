"""Example usage of __init_subclass__ plugin framework."""

from framework import Application, Plugin


class PluginA(Plugin):
    def run(self, app: Application) -> None:
        print('PluginA running!')


class PluginB(Plugin):
    def run(self, app: Application) -> None:
        print('PluginB running!')


class PluginC(Plugin):
    def run(self, app: Application) -> None:
        print('PluginC running!')


if __name__ == '__main__':
    app = Application()
    app.run()
