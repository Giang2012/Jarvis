from gui.animation.animation import Animation
from gui.animation.easing import Easing


class MoveAnimation(Animation):

    def __init__(

        self,

        x1,

        y1,

        x2,

        y2,

        duration=1000

    ):

        super().__init__(duration)

        self.x1 = x1
        self.y1 = y1

        self.x2 = x2
        self.y2 = y2

    def position(self):

        t = Easing.easeInOut(

            self.value

        )

        x = self.x1 + (

            self.x2 - self.x1

        ) * t

        y = self.y1 + (

            self.y2 - self.y1

        ) * t

        return x, y