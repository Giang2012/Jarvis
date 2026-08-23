class Timeline:

    def __init__(self):

        self.current = 0

    def next(self):

        self.current += 1

    def reset(self):

        self.current = 0