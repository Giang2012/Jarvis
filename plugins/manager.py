class PluginManager:

    def __init__(self):

        self.plugins = {}

    def register(self, plugin):

        self.plugins[plugin.name] = plugin

        plugin.on_load()

    def unload(self, name):

        if name in self.plugins:

            self.plugins[name].on_unload()

            del self.plugins[name]