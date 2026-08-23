from core.brain import Brain


brain = Brain()


while True:

    text = input(">>> ")

    if text.lower().strip() in ["exit", "quit", "thoát"]:
        print("JARVIS: Goodbye.")
        break

    if not text.strip():
        continue

    print()

    try:

        reply = brain.process(text)

        print(f"[JARVIS] {reply}")

    except Exception as e:

        print(f"[JARVIS ERROR] {e}")

    print()