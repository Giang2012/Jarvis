from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QTextEdit, QGridLayout, QFrame
)


class ToolDetail(QWidget):
    """Reusable detail surface shown when a tool is selected."""

    def __init__(self, title, description, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(22, 20, 22, 22)
        layout.setSpacing(14)

        title_label = QLabel(title)
        title_label.setStyleSheet(
            'color:#dffcff; font:700 18pt "Segoe UI";'
        )

        desc = QLabel(description)
        desc.setWordWrap(True)
        desc.setStyleSheet(
            'color:#76aeb8; font:10pt "Segoe UI";'
        )

        layout.addWidget(title_label)
        layout.addWidget(desc)

        self.body = QFrame()
        self.body.setStyleSheet("""
            QFrame {
                background: rgba(3, 14, 23, 205);
                border: 1px solid rgba(0, 205, 235, 80);
                border-radius: 10px;
            }
        """)
        self.body_layout = QVBoxLayout(self.body)
        self.body_layout.setContentsMargins(18, 18, 18, 18)
        self.body_layout.setSpacing(12)
        layout.addWidget(self.body, 1)


def build_tool_detail(key: str, tool, parent=None):
    detail = ToolDetail(tool.title, tool.description, parent)
    body = detail.body_layout

    if key == "weather":
        row = QHBoxLayout()
        city = QComboBox()
        city.addItems(["Hanoi", "Ho Chi Minh City", "Da Nang", "Tokyo", "London"])
        refresh = QPushButton("REFRESH")
        row.addWidget(QLabel("LOCATION"))
        row.addWidget(city, 1)
        row.addWidget(refresh)
        body.addLayout(row)

        temp = QLabel("28° C")
        temp.setStyleSheet('color:#72f6ff; font:700 32pt "Segoe UI";')
        condition = QLabel("Light Rain  •  Humidity 72%  •  Wind 8 km/h")
        condition.setStyleSheet('color:#9bc7cf; font:10pt "Segoe UI";')
        body.addWidget(temp)
        body.addWidget(condition)
        body.addStretch()

    elif key == "calculator":
        edit = QLineEdit()
        edit.setPlaceholderText("Enter expression…")
        result = QLabel("READY")
        result.setStyleSheet('color:#6ff4ff; font:700 16pt "Segoe UI";')
        button = QPushButton("CALCULATE")
        body.addWidget(edit)
        body.addWidget(button)
        body.addWidget(result)
        body.addStretch()

    elif key == "search":
        edit = QLineEdit()
        edit.setPlaceholderText("Search the web…")
        button = QPushButton("SEARCH")
        body.addWidget(edit)
        body.addWidget(button)
        body.addStretch()

    elif key == "ai_chat":
        prompt = QLineEdit()
        prompt.setPlaceholderText("Ask JARVIS…")
        send = QPushButton("SEND")
        body.addWidget(prompt)
        body.addWidget(send)
        body.addStretch()

    elif key == "open_app":
        app = QComboBox()
        app.addItems(["Chrome", "VS Code", "Discord", "File Explorer"])
        launch = QPushButton("LAUNCH")
        body.addWidget(app)
        body.addWidget(launch)
        body.addStretch()

    elif key == "notes":
        editor = QTextEdit()
        editor.setPlaceholderText("Write a note…")
        body.addWidget(editor, 1)
        body.addWidget(QPushButton("SAVE NOTE"))

    else:
        status = QLabel("MODULE READY")
        status.setStyleSheet(
            'color:#72f6ff; font:700 12pt "Segoe UI";'
        )
        body.addWidget(status)
        body.addWidget(QLabel(
            "This module is registered and ready for its service adapter."
        ))
        body.addStretch()

    detail.setStyleSheet("""
        QLineEdit, QTextEdit, QComboBox {
            color: #dffcff;
            background: rgba(4, 21, 31, 230);
            border: 1px solid rgba(0, 205, 235, 110);
            border-radius: 7px;
            padding: 9px;
            font: 10pt "Segoe UI";
        }
        QPushButton {
            color: #cfffff;
            background: rgba(0, 180, 220, 38);
            border: 1px solid rgba(0, 225, 255, 120);
            border-radius: 7px;
            padding: 9px 16px;
            font: 700 9pt "Segoe UI";
        }
        QPushButton:hover {
            background: rgba(0, 205, 240, 70);
            border: 1px solid rgba(80, 245, 255, 210);
        }
        QLabel {
            color: #79aeb8;
            font: 9pt "Segoe UI";
        }
    """)
    return detail
