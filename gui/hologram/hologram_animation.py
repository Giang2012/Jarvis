class HologramAnimation:

    def __init__(self):

        self.hover = 0

        self.targetHover = 0

        self.scale = 1

        self.targetScale = 1

    # -------------------------

    def update(self):

        self.hover += (

            self.targetHover - self.hover

        ) * 0.12

        self.scale += (

            self.targetScale - self.scale

        ) * 0.12

    # -------------------------

    def enter(self):

        self.targetHover = 1

        self.targetScale = 1.03

    # -------------------------

    def leave(self):

        self.targetHover = 0

        self.targetScale = 1