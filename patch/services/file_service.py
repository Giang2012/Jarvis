import os
import subprocess
from pathlib import Path


class FileService:
    def list_dir(self, path=None):
        target = Path(path or Path.home()).expanduser().resolve()
        if not target.exists():
            return []
        return [
            {
                "name": p.name,
                "path": str(p),
                "directory": p.is_dir(),
            }
            for p in sorted(target.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))
        ]

    def open(self, path):
        target = Path(path).expanduser()
        if not target.exists():
            return f"Path does not exist: {target}"
        try:
            os.startfile(str(target))
            return f"Opened {target}."
        except Exception as exc:
            return f"Could not open {target}: {exc}"

    def search(self, query, root=None, limit=100):
        query = str(query or "").strip().lower()
        base = Path(root or Path.home()).expanduser()
        if not query or not base.exists():
            return []
        results = []
        try:
            for path in base.rglob("*"):
                if query in path.name.lower():
                    results.append(str(path))
                    if len(results) >= limit:
                        break
        except (PermissionError, OSError):
            pass
        return results
