import json


class Settings:

    def __init__(self):

        with open("config/settings.json", encoding="utf-8") as file:

            self.data = json.load(file)

    def get_username(self):

        return self.data["username"]