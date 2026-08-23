from gui.animation.animation import Animation
from gui.animation.easing import Easing


class OpacityAnimation(Animation):

    def __init__(

        self,

        start=0,

        end=1,

        duration=1000

    ):

        super().__init__(duration)

        self.startValue = start
        self.endValue = end

    def opacity(self):

        t = Easing.easeOut(self.value)

        return self.startValue + (

            self.endValue - self.startValue

        ) * t