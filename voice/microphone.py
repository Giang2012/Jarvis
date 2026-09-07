import os
import audioop
import pyaudio
import speech_recognition as sr


class Microphone:
    def __init__(self):
        self.device_index = int(
            os.getenv("JARVIS_MIC_DEVICE_INDEX", "21")
        )

        self.rate = 16000
        self.channels = 1
        self.chunk = 1024

        self.threshold = int(
            os.getenv("JARVIS_MIC_THRESHOLD", "500")
        )

        self.timeout = 10
        self.phrase_time_limit = 10

        self.audio = pyaudio.PyAudio()
        self.stream = None

        self._validate_device()

    def _validate_device(self):
        info = self.audio.get_device_info_by_index(
            self.device_index
        )

        if int(info.get("maxInputChannels", 0)) < 1:
            raise RuntimeError(
                f"Device {self.device_index} không có input."
            )

        print(
            "[JARVIS MIC] Device:",
            self.device_index
        )
        print(
            "[JARVIS MIC] Name:",
            info.get("name")
        )
        print(
            "[JARVIS MIC] Rate:",
            self.rate
        )
        print(
            "[JARVIS MIC] Threshold:",
            self.threshold
        )

    def _open(self):
        if self.stream is not None:
            return

        self.stream = self.audio.open(
            format=pyaudio.paInt16,
            channels=self.channels,
            rate=self.rate,
            input=True,
            input_device_index=self.device_index,
            frames_per_buffer=self.chunk,
        )

    def listen(self):
        self._open()

        recognizer = sr.Recognizer()

        frames = []
        started = False
        silent_chunks = 0

        max_chunks = int(
            self.phrase_time_limit
            * self.rate
            / self.chunk
        )

        print("[JARVIS MIC] Đang nghe...")

        for _ in range(max_chunks):
            data = self.stream.read(
                self.chunk,
                exception_on_overflow=False,
            )

            rms = audioop.rms(data, 2)

            if rms >= self.threshold:
                started = True
                silent_chunks = 0
                frames.append(data)

            elif started:
                frames.append(data)
                silent_chunks += 1

                # khoảng 0.8 giây im lặng => kết thúc câu
                if silent_chunks >= int(
                    1.2 * self.rate / self.chunk
                ):
                    break

        if not frames:
            return None

        raw_audio = b"".join(frames)

        print(
            f"[JARVIS MIC] Captured "
            f"{len(raw_audio)} bytes"
        )

        return sr.AudioData(
            raw_audio,
            self.rate,
            2,
        )

    def close(self):
        if self.stream is not None:
            try:
                self.stream.stop_stream()
            except Exception:
                pass

            try:
                self.stream.close()
            except Exception:
                pass

            self.stream = None

        if self.audio is not None:
            try:
                self.audio.terminate()
            except Exception:
                pass

            self.audio = None