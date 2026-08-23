from gui.animation.animation import Animation
from gui.animation.easing import Easing


class RotationAnimation(Animation):

    def __init__(

        self,

        start,

        end,

        duration=1000

    ):

        super().__init__(duration)

        self.startAngle = start
        self.endAngle = end

    def angle(self):

        t = Easing.easeInOut(

            self.value

        )

        return self.startAngle + (

            self.endAngle -

            self.startAngle

        ) * t