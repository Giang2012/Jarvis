import sounddevice as sd
import numpy as np
import wave


mic_id = 11  # microphone của bạn

duration = 5
sample_rate = 44100

print("JARVIS đang nghe...")

audio = sd.rec(
    int(duration * sample_rate),
    samplerate=sample_rate,
    channels=1,
    dtype=np.int16,
    device=mic_id
)

sd.wait()

print("Đã nghe xong!")

with wave.open("test_voice.wav", "wb") as file:
    file.setnchannels(1)
    file.setsampwidth(2)
    file.setframerate(sample_rate)
    file.writeframes(audio.tobytes())

print("Đã lưu file test_voice.wav")
