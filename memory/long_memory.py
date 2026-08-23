import json
import os


class LongMemory:

    FILE = "memory/data.json"

    def __init__(self):

        if not os.path.exists(self.FILE):

            with open(self.FILE, "w") as f:

                json.dump({}, f)

    def save(self, key, value):

        data = self.load()

        data[key] = value

        with open(self.FILE, "w") as f:

            json.dump(data, f, indent=4)

    def load(self):

        with open(self.FILE) as f:

            return json.load(f)