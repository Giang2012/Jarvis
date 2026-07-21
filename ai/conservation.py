class Conversation:

    def __init__(self):

        self.history=[]

    def add_user(self,text):

        self.history.append(
            {
                "role":"user",
                "content":text
            }
        )

    def add_ai(self,text):

        self.history.append(
            {
                "role":"assistant",
                "content":text
            }
        )

    def build_prompt(self):

        prompt=""

        for msg in self.history:

            prompt+=f"{msg['role']}:{msg['content']}\n"

        return prompt