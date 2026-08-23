from pathlib import Path

from PySide6.QtSvg import QSvgRenderer


class SVGLoader:

    _cache = {}

    @classmethod
    def load(cls, file):

        path = str(Path(file))

        if path not in cls._cache:

            cls._cache[path] = QSvgRenderer(path)

        return cls._cache[path]