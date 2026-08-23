from gui.animation.animation import Animation
from gui.animation.easing import Easing


class ScaleAnimation(Animation):

    def __init__(

        self,

        start,

        end,

        duration=1000

    ):

        super().__init__(duration)

        self.startScale = start
        self.endScale = end

    def scale(self):

        t = Easing.easeOut(

            self.value

        )

        return self.startScale + (

            self.endScale -

            self.startScale

        ) * t