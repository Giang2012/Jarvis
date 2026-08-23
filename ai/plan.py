class Plan:

    def __init__(self):

        self.tasks = []

    def add(self, task):

        self.tasks.append(task)

    def __iter__(self):

        return iter(self.tasks)