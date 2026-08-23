from skills.base_skill import BaseSkill


class WeatherSkill(BaseSkill):

    name = "WEATHER"

    def execute(self, text):

        return (
            "Weather Service chưa được kết nối API. "
            "Phần này sẽ được nối vào hệ thống thời tiết sau."
        )