class ThemeManager:

    mode = AIMode.NORMAL

    def set_mode(self, mode):

        self.mode = mode

    def get(self):

        return THEMES[self.mode]