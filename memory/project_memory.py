import json
import os


class ProjectMemory:

    FILE = "memory/projects.json"

    def __init__(self):

        self.projects = {}

        self._load()

    # =========================================================
    # LOAD
    # =========================================================

    def _load(self):

        if not os.path.exists(self.FILE):

            self._save()

            return

        try:

            with open(
                self.FILE,
                "r",
                encoding="utf-8"
            ) as f:

                data = json.load(f)

            if isinstance(data, dict):

                self.projects = data

        except Exception:

            self.projects = {}

    # =========================================================
    # SAVE
    # =========================================================

    def _save(self):

        os.makedirs(
            os.path.dirname(self.FILE),
            exist_ok=True
        )

        with open(
            self.FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                self.projects,
                f,
                ensure_ascii=False,
                indent=4
            )

    # =========================================================
    # UPDATE
    # =========================================================

    def update(self, name, status):

        if not name:
            return

        self.projects[name] = status

        self._save()

    # =========================================================
    # GET
    # =========================================================

    def get(self, name):

        return self.projects.get(
            name
        )

    # =========================================================
    # ALL
    # =========================================================

    def all(self):

        return dict(
            self.projects
        )

    # =========================================================
    # REMOVE
    # =========================================================

    def remove(self, name):

        if name not in self.projects:
            return False

        del self.projects[name]

        self._save()

        return True

    # =========================================================
    # CLEAR
    # =========================================================

    def clear(self):

        self.projects.clear()

        self._save()