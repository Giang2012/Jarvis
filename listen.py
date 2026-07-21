import sounddevice as sd
import speech_recognition as sr
import numpy as np


mic_id = 11
sample_rate = 44100
duration = 5


print("JARVIS đang nghe...")


audio = sd.rec(
    int(duration * sample_rate),
    samplerate=sample_rate,
    channels=1,
    dtype=np.int16,
    device=mic_id
)

sd.wait()


print("Đang xử lý...")


recognizer = sr.Recognizer()

audio_data = sr.AudioData(
    audio.tobytes(),
    sample_rate,
    2
)


try:
    text = recognizer.recognize_google(
        audio_data,
        language="vi-VN"
    )

    print("Bạn nói:", text)


except Exception as e:
    print("Không nghe rõ:", e)