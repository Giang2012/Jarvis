import importlib
import pkgutil

import plugins


class PluginManager:

    def __init__(self):

        self.plugins = {}

    def load(self):

        for _, module_name, _ in pkgutil.iter_modules(

            plugins.__path__

        ):

            module = importlib.import_module(

                f"plugins.{module_name}"

            )

            if hasattr(module, "Plugin"):

                obj = module.Plugin()

                self.plugins[obj.name] = obj