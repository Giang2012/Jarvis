class ProjectMemory:

    def __init__(self):

        self.projects = {}

    def update(self, name, status):

        self.projects[name] = status

    def get(self, name):

        return self.projects.get(name)