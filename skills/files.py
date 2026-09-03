from skills.base_skill import BaseSkill


class FileSkill(BaseSkill):
    def __init__(self, files):
        super().__init__()
        self.name = "FILES"
        self.files = files

    def execute(self, text):
        text = str(text or "").strip()
        lower = text.lower()
        if lower.startswith("list:"):
            items = self.files.list_dir(text.split(":", 1)[1].strip() or None)
            return "\n".join(x["path"] for x in items[:80])
        if lower.startswith("open:"):
            return self.files.open(text.split(":", 1)[1].strip())
        if lower.startswith("search:"):
            results = self.files.search(text.split(":", 1)[1].strip())
            return "\n".join(results[:100])
        return "File command not recognized."
