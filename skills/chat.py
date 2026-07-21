from ai.chatbot import ChatBot


class ChatSkill:

    def __init__(self):
        self.bot = ChatBot()

    def run(self, text):
        return self.bot.ask(text)