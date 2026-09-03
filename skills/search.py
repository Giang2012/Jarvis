from skills.base_skill import BaseSkill


class SearchSkill(BaseSkill):

    name = "SEARCH"

    PREFIXES = [
        "tìm kiếm",
        "tìm",
        "search for",
        "search",
        "google",
        "tra cứu",
        "hãy tìm",
    ]

    def __init__(self, browser_service=None):

        self.browser = browser_service

    def execute(self, text):

        if text is None:
            return "Không có nội dung tìm kiếm."

        query = str(text).strip()

        if not query:
            return "Không có nội dung tìm kiếm."

        lowered = query.lower()

        for prefix in self.PREFIXES:

            if lowered.startswith(prefix):

                query = query[len(prefix):].strip()

                break

        if not query:
            return "Không có nội dung tìm kiếm."

        if self.browser is None:
            return "Dịch vụ trình duyệt chưa sẵn sàng."

        success = self.browser.search(query)

        if success:
            return f"Đang tìm kiếm {query}."

        return f"Không thể tìm kiếm {query}."