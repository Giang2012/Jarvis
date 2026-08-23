import os
import importlib


class PluginLoader:

    def __init__(self, manager):

        self.manager = manager

    def load_plugins(self):

        folder = "plugins"

        for file in os.listdir(folder):

            if not file.endswith(".py"):
                continue

            if file.startswith("__"):
                continue

            if file in [
                "plugin.py",
                "loader.py",
                "manager.py"
            ]:
                continue

            module = importlib.import_module(

                f"plugins.{file[:-3]}"

            )

            plugin = module.PluginMain()

            self.manager.register(plugin)