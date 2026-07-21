def save(user, jarvis):

    with open("data/history.txt", "a", encoding="utf-8") as file:

        file.write(f"Bạn: {user}\n")

        file.write(f"Jarvis: {jarvis}\n\n")