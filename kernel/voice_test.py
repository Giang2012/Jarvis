import os
from services.voice_service import VoiceService


def main():
    voice = VoiceService()

    if not voice.api_key:
        raise SystemExit(
            "Missing ELEVENLABS_API_KEY. Set the environment variable first."
        )

    if not voice.voice_id:
        raise SystemExit(
            "Missing ELEVENLABS_VOICE_ID. Set the environment variable first."
        )

    print("JARVIS VOICE TEST")
    print("Speak after the recording starts...")
    text = voice.listen_once(seconds=5)

    print("YOU:", text or "(nothing recognized)")

    if text:
        reply = f"Đã nghe thấy: {text}"
        print("JARVIS:", reply)
        voice.speak(reply)

    print("VOICE TEST: PASS")


if __name__ == "__main__":
    main()
