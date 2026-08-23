from PySide6.QtCore import QObject, QTimer


class Timeline(QObject):

    def __init__(self):

        super().__init__()

        self.time = 0

        self.timer = QTimer()

        self.timer.timeout.connect(self.update)

        self.timer.start(16)

    def update(self):

        self.time += 16

    def between(self,start,end):

        return start <= self.time < end

    def after(self,t):

        return self.time >= t

    def reset(self):

        self.time = 0