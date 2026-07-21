from ai.chatbot import ChatBot

bot = ChatBot()

while True:
    text = input("Bạn: ")

    if text == "exit":
        break

    answer = bot.ask(text)

    print("\nJarvis:", answer)