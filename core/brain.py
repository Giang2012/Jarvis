from core.logger import write
from core.settings import Settings
from core.ai import AI
from skills.open_app import OpenAppSkill
from core.registry import COMMANDS

from skills.search_google import run as google_search
from skills.search_youtube import run as youtube_search


class Brain:
   
    def __init__(self):
        self.settings = Settings()
        self.ai = AI()  
    def think(self, command):
        write(command)  
        text = command.lower()
        if "cảm ơn" in text:

            return "Rất vui được giúp bạn."

        if "xin chào" in text:

            return (
                f"Xin chào "
                f"{self.settings.get_username()}!"
            )
        
        if "tạm biệt" in text:

            return "Hẹn gặp lại!"

        if text.startswith("tìm google "):

            return google_search(command[11:])

        if text.startswith("tìm youtube "):

            return youtube_search(command[12:])

        for keyword, action in COMMANDS.items():

            if keyword in text:

                return action()
        answer = open_app(command)

        if answer:  
         return answer
         
        return self.ai.chat(command)
    from skills.open_app import OpenAppSkill


class Brain:

    def __init__(self):
        self.open_app_skill = OpenAppSkill()


    def think(self, text):

        if "mở" in text:
            return self.open_app_skill.run(text)

        return "Tôi chưa hiểu yêu cầu."