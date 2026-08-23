import random


class CameraShake:

    def __init__(self):

        self.power = 0

    # ============================

    def shake(self, amount):

        if amount > self.power:
            self.power = amount

    # ============================

    def update(self):

        if self.power > 0:

            self.power *= 0.90

        if self.power < 0.2:

            self.power = 0

    # ============================

    def offset(self):

        self.update()

        return (

            random.uniform(-self.power, self.power),

            random.uniform(-self.power, self.power)

        )