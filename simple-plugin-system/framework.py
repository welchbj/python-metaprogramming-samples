"""Example __init_subclass__ based plugin framework."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Type


class Application:

    def run(self) -> None:
        """Run all of this application's plugins."""
        for plugin_cls in Plugin.registered_plugins:
            plugin = plugin_cls()
            plugin.run(self)


class Plugin(ABC):

    registered_plugins: List[Type[Plugin]] = []

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()

        # Record loaded plugins.
        Plugin.registered_plugins.append(cls)

    @abstractmethod
    def run(self, app: Application) -> None:
        """Run this plugin, mutating the application."""
