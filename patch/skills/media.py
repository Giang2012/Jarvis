from skills.base_skill import BaseSkill


class MediaSkill(BaseSkill):
    def __init__(self, media):
        super().__init__()
        self.name = "MEDIA"
        self.media = media

    def execute(self, text):
        return self.media.key(text)
