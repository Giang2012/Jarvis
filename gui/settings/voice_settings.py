from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QPushButton,
    QMessageBox,
)


VOICES = {
    "Voice 1": "hNe03uL2BbiU3txTclei.",
    "Voice 2": "ev2kMR9ZJZZsemuogS5u.",
}


class VoiceSettingsDialog(QDialog):

    def __init__(
        self,
        brain,
        parent=None
    ):

        super().__init__(parent)

        self.brain = brain

        self.setWindowTitle(
            "JARVIS Voice"
        )

        self.resize(
            520,
            230
        )

        self.setStyleSheet(
            """
            QDialog {
                background: #05070a;
                color: #d9e7f5;
            }

            QLabel {
                color: #9db0c5;
                font-size: 14px;
            }

            QComboBox,
            QPushButton {
                background: #0c1118;
                color: #d9e7f5;
                border: 1px solid #26384b;
                padding: 8px;
            }

            QPushButton:hover {
                border: 1px solid #5aa9ff;
            }
            """
        )

        layout = QVBoxLayout(
            self
        )

        # Provider

        layout.addWidget(
            QLabel("TTS Provider")
        )

        layout.addWidget(
            QLabel("ElevenLabs")
        )

        # Voice

        layout.addWidget(
            QLabel("Voice")
        )

        self.voice_combo = QComboBox()

        self.voice_combo.addItems(
            VOICES.keys()
        )

        current_id = getattr(
            getattr(
                getattr(
                    self.brain,
                    "voice",
                    None
                ),
                "tts",
                None
            ),
            "voice_id",
            ""
        )

        for index, (
            name,
            voice_id
        ) in enumerate(
            VOICES.items()
        ):

            if voice_id == current_id:

                self.voice_combo.setCurrentIndex(
                    index
                )

                break

        layout.addWidget(
            self.voice_combo
        )

        # Buttons

        row = QHBoxLayout()

        test_button = QPushButton(
            "Test Voice"
        )

        save_button = QPushButton(
            "Save"
        )

        close_button = QPushButton(
            "Close"
        )

        row.addWidget(
            test_button
        )

        row.addStretch()

        row.addWidget(
            save_button
        )

        row.addWidget(
            close_button
        )

        layout.addLayout(
            row
        )

        # Events

        test_button.clicked.connect(
            self.test_voice
        )

        save_button.clicked.connect(
            self.save_voice
        )

        close_button.clicked.connect(
            self.close
        )

    # =========================
    # VOICE ID
    # =========================

    def selected_voice_id(self):

        return VOICES[
            self.voice_combo.currentText()
        ]

    # =========================
    # APPLY
    # =========================

    def _apply_voice(self):

        voice = getattr(
            self.brain,
            "voice",
            None
        )

        if voice is None:

            raise RuntimeError(
                "Brain.voice chưa được khởi tạo."
            )

        manager = getattr(
            voice,
            "tts",
            None
        )

        if manager is None:

            raise RuntimeError(
                "Voice provider manager chưa được khởi tạo."
            )

        manager.voice_id = (
            self.selected_voice_id()
        )

        manager.provider = (
            manager._build()
        )

    # =========================
    # TEST
    # =========================

    def test_voice(self):

        try:

            self._apply_voice()

            self.brain.voice.speak(
                "Xin chào. Tôi là JARVIS."
            )

        except Exception as exc:

            QMessageBox.critical(
                self,
                "Voice error",
                str(exc)
            )

    # =========================
    # SAVE
    # =========================

    def save_voice(self):

        try:

            self._apply_voice()

            QMessageBox.information(
                self,
                "JARVIS",
                "Voice đã được chọn."
            )

        except Exception as exc:

            QMessageBox.critical(
                self,
                "Voice error",
                str(exc)
            )