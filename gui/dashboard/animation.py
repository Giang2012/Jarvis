class DashboardAnimation:

    def __init__(self):

        self.progress = 0.0

        self.target = 1.0

        self.speed = 0.04

    # -------------------------------------

    def update(self):

        self.progress += (
            self.target - self.progress
        ) * self.speed

    # -------------------------------------

    def show(self):

        self.target = 1.0

    # -------------------------------------

    def hide(self):

        self.target = 0.0