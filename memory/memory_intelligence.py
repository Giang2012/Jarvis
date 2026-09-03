import re


class MemoryIntelligence:

    """
    Bộ điều phối memory của JARVIS.

    Nhiệm vụ:

    1. Phát hiện thông tin người dùng muốn lưu.
    2. Phát hiện thông tin project.
    3. Lấy memory liên quan.
    4. Không biến mọi câu chat thành long-term memory.
    """

    # =========================================================
    # USER MEMORY PATTERNS
    # =========================================================

    USER_PATTERNS = {

        "name": [
            r"(?:tôi|tao|mình)\s+(?:tên|la)\s+(?:là\s+)?(.+)",
            r"(?:tôi|tao|mình)\s+ tên\s+(.+)",
        ],

        "nickname": [
            r"(?:gọi|hãy gọi)\s+(?:tôi|tao|mình)\s+(?:là\s+)?(.+)",
        ],

        "preference": [
            r"(?:tôi|tao|mình)\s+(?:thích|thường thích)\s+(.+)",
        ],
    }

    # =========================================================
    # PROJECT PATTERNS
    # =========================================================

    PROJECT_PATTERNS = [

        r"(?:đang|hiện đang)\s+làm\s+(?:project|dự án)\s+(.+)",

        r"(?:project|dự án)\s+(?:của\s+)?(?:tôi|tao|mình)\s+(?:là|về)\s+(.+)",

        r"(?:tiếp tục|quay lại)\s+(?:project|dự án)\s+(.+)",
    ]

    # =========================================================
    # IMPORTANT MEMORY
    # =========================================================

    IMPORTANT_PREFIXES = [

        "nhớ rằng",
        "hãy nhớ",
        "ghi nhớ",
        "nhớ giúp",
        "lưu lại",
        "đừng quên",
    ]

    def __init__(self, memory):

        self.memory = memory

    # =========================================================
    # PROCESS INPUT
    # =========================================================

    def process(self, text):

        if not text:
            return

        clean = text.strip()

        if not clean:
            return

        # -----------------------------------------------------
        # USER INFORMATION
        # -----------------------------------------------------

        self._detect_user(clean)

        # -----------------------------------------------------
        # PROJECT INFORMATION
        # -----------------------------------------------------

        self._detect_project(clean)

        # -----------------------------------------------------
        # EXPLICIT MEMORY
        # -----------------------------------------------------

        self._detect_explicit_memory(clean)

    # =========================================================
    # USER DETECTION
    # =========================================================

    def _detect_user(self, text):

        lower = text.lower()

        for key, patterns in self.USER_PATTERNS.items():

            for pattern in patterns:

                match = re.search(
                    pattern,
                    lower,
                    re.IGNORECASE
                )

                if not match:
                    continue

                value = match.group(
                    1
                ).strip()

                if not value:
                    continue

                # Không lưu câu quá dài thành profile.
                if len(value) > 100:
                    continue

                self.memory.set_user(
                    key,
                    value
                )

                return

    # =========================================================
    # PROJECT DETECTION
    # =========================================================

    def _detect_project(self, text):

        for pattern in self.PROJECT_PATTERNS:

            match = re.search(
                pattern,
                text,
                re.IGNORECASE
            )

            if not match:
                continue

            project = match.group(
                1
            ).strip()

            if not project:
                continue

            if len(project) > 100:
                continue

            self.memory.update_project(
                project,
                "active"
            )

            return

    # =========================================================
    # EXPLICIT MEMORY
    # =========================================================

    def _detect_explicit_memory(self, text):

        lower = text.lower()

        for prefix in self.IMPORTANT_PREFIXES:

            if not lower.startswith(prefix):
                continue

            content = text[
                len(prefix):
            ].strip()

            if not content:
                return

            self.memory.save(
                self._make_memory_key(
                    content
                ),
                {
                    "type": "explicit",
                    "content": content
                }
            )

            return

    # =========================================================
    # MEMORY KEY
    # =========================================================

    def _make_memory_key(self, text):

        normalized = text.lower().strip()

        normalized = re.sub(
            r"\s+",
            "_",
            normalized
        )

        normalized = re.sub(
            r"[^a-zA-Z0-9_\u00C0-\u1EF9]",
            "",
            normalized
        )

        return (
            "memory_"
            + normalized[:80]
        )

    # =========================================================
    # BUILD CONTEXT
    # =========================================================

    def build_context(self):

        sections = []

        # -----------------------------------------------------
        # USER
        # -----------------------------------------------------

        user_context = []

        name = self.memory.get_user(
            "name"
        )

        nickname = self.memory.get_user(
            "nickname"
        )

        preference = self.memory.get_user(
            "preference"
        )

        if name:
            user_context.append(
                f"Tên chủ nhân: {name}"
            )

        if nickname:
            user_context.append(
                f"Cách gọi: {nickname}"
            )

        if preference:
            user_context.append(
                f"Sở thích: {preference}"
            )

        if user_context:

            sections.append(
                "[USER MEMORY]\n"
                + "\n".join(user_context)
            )

        # -----------------------------------------------------
        # PROJECT
        # -----------------------------------------------------

        projects = self.memory.project.projects

        if projects:

            project_lines = []

            for name, status in projects.items():

                project_lines.append(
                    f"- {name}: {status}"
                )

            sections.append(
                "[PROJECT MEMORY]\n"
                + "\n".join(project_lines)
            )

        # -----------------------------------------------------
        # LONG MEMORY
        # -----------------------------------------------------

        long_data = self.memory.load()

        explicit = []

        for key, value in long_data.items():

            if not isinstance(value, dict):
                continue

            if value.get("type") != "explicit":
                continue

            content = value.get(
                "content"
            )

            if content:
                explicit.append(
                    f"- {content}"
                )

        if explicit:

            sections.append(
                "[LONG-TERM MEMORY]\n"
                + "\n".join(explicit[-20:])
            )

        if not sections:

            return ""

        return (
            "\n\n".join(sections)
        )