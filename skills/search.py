from skills.base_skill import BaseSkill


class SearchSkill(BaseSkill):

    name = "SEARCH"

    PREFIXES = [
        "tìm kiếm",
        "tìm",
        "search",
        "google",
        "tra cứu",
        "hãy tìm",
    ]

    def __init__(self, browser_service=None):

        self.browser = browser_service

    def execute(self, text):

        query = text.lower().strip()

        for prefix in self.PREFIXES:

            if query.startswith(prefix):

                query = query[len(prefix):].strip()

                break

        if not query:

            return "Bạn muốn tôi tìm gì?"

        if self.browser is None:

            return "Dịch vụ trình duyệt chưa sẵn sàng."

        success = self.browser.search(query)

        if success:

            return f"Đang tìm kiếm {query}."

        return "Không thể mở trình duyệt."