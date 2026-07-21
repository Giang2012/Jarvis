from ai.chatbot import ChatBot


class AIManager:

    def __init__(self):

        self.chatbot = ChatBot()

    def ask(self, text):

        return self.chatbot.ask(text)