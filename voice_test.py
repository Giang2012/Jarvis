from services.voice_service import VoiceService

print("=" * 50)
print("       J.A.R.V.I.S VOICE TEST")
print("=" * 50)

voice = VoiceService()

print()
print("Microphone device : 20")
print("Sample rate       :", voice.sample_rate)
print("Channels          :", voice.channels)
print()

print(">>> JARVIS DANG NGHE <<<")
print("Hay noi mot cau tieng Viet...")
print("(5 giay)")

try:
    text = voice.listen_once(seconds=5)

    print()
    print("-" * 50)

    if text:
        print("BAN NOI:")
        print(text)
    else:
        print("JARVIS khong nghe thay gi.")

except Exception as e:
    print()
    print("LOI:")
    print(type(e).__name__, e)