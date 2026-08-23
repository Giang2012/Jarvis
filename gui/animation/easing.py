class Easing:

    @staticmethod
    def linear(t):

        return t

    @staticmethod
    def easeIn(t):

        return t * t

    @staticmethod
    def easeOut(t):

        return 1 - (1 - t) * (1 - t)

    @staticmethod
    def easeInOut(t):

        if t < .5:

            return 2 * t * t

        return 1 - pow(-2 * t + 2, 2) / 2