from PySide6.QtWidgets import (
    QWidget,
    QTextEdit,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
)

from PySide6.QtCore import Qt


class ChatWidget(QWidget):

    def __init__(self, brain):
        super().__init__()

        self.brain = brain

        self.build_ui()
        self.setStyleSheet("""
        QWidget{
            background:#101820;
            border:2px solid red;
        }

        QTextEdit{
            background:#182632;
            color:white;
        }

        QLineEdit{
            background:#182632;
            color:white;
        }

        QPushButton{
            background:#00D8FF;
        }
        """)
        print(self.geometry())
    def build_ui(self):

        layout = QVBoxLayout(self)

        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(10)

        self.history = QTextEdit()
        self.history.setReadOnly(True)

        self.history.setText(
            "🤖 JARVIS đã sẵn sàng...\n"
        )

        self.input = QLineEdit()

        self.input.setPlaceholderText(
            "Nhập lệnh cho Jarvis..."
        )

        self.send = QPushButton("➜")

        bottom = QHBoxLayout()

        bottom.addWidget(self.input)
        bottom.addWidget(self.send)

        layout.addWidget(self.history)
        layout.addLayout(bottom)

        self.setMinimumHeight(220)
        self.setMaximumHeight(220)

        self.send.clicked.connect(
            self.send_message
        )

        self.input.returnPressed.connect(
            self.send_message
        )

    def send_message(self):

        text = self.input.text().strip()

        if not text:
            return

        self.history.append(
            f"<font color='#00D8FF'><b>Bạn:</b></font> {text}"
        )

        reply = self.brain.process(text)

        self.history.append(
            f"<font color='white'><b>Jarvis:</b></font> {reply}"
        )

        self.input.clear()