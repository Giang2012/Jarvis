from plugins.plugin import Plugin


class PluginMain(Plugin):

    name = "Example"

    version = "1.0"

    author = "Tam"

    def on_load(self):

        print(

            "Example Loaded"

        )

    def on_unload(self):

        print(

            "Example Unloaded"

        )