import os
import tempfile
import urllib.request
import urllib.error
import subprocess
import platform

from .base import TTSProvider


class ElevenLabsTTS(TTSProvider):
    """Minimal ElevenLabs REST adapter.

    The API key is read from ELEVENLABS_API_KEY and is never stored in source.
    Voice IDs are configurable through JARVIS_VOICE_ID.
    """

    def __init__(self, voice_id: str, model_id: str = "eleven_multilingual_v2"):
        self.voice_id = voice_id
        self.model_id = model_id
        self.api_key = os.getenv("ELEVENLABS_API_KEY", "").strip()
        if not self.api_key:
            raise RuntimeError(
                "ELEVENLABS_API_KEY is missing. Put it in your local .env/environment."
            )

    def speak(self, text: str) -> None:
        if not text:
            return

        url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice_id}"
        payload = (
            '{"text":' + _json_quote(text) +
            ',"model_id":' + _json_quote(self.model_id) + "}"
        ).encode("utf-8")

        req = urllib.request.Request(
            url,
            data=payload,
            headers={
                "xi-api-key": self.api_key,
                "Content-Type": "application/json",
                "Accept": "audio/mpeg",
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                audio = response.read()
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(
                f"ElevenLabs TTS HTTP {exc.code}: {body[:300]}"
            ) from exc

        fd, path = tempfile.mkstemp(suffix=".mp3", prefix="jarvis_tts_")
        os.close(fd)
        try:
            with open(path, "wb") as f:
                f.write(audio)
            _play_audio(path)
        finally:
            try:
                os.remove(path)
            except OSError:
                pass


def _json_quote(value: str) -> str:
    import json
    return json.dumps(value, ensure_ascii=False)


def _play_audio(path: str) -> None:
    system = platform.system()
    if system == "Windows":
        import winsound
        # winsound cannot play MP3 directly, so use PowerShell MediaPlayer.
        ps = (
            "$p=New-Object System.Windows.Media.MediaPlayer;"
            f"$p.Open([uri]'{path.replace(chr(39), chr(39)+chr(39))}');"
            "$p.Play(); Start-Sleep -Milliseconds 200;"
            "while($p.Position -lt $p.NaturalDuration.TimeSpan){Start-Sleep -Milliseconds 100};"
            "$p.Close()"
        )
        subprocess.run(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps],
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    elif system == "Darwin":
        subprocess.run(["afplay", path], check=False)
    else:
        for player in ("mpg123", "ffplay", "mpv"):
            if shutil_which := __import__("shutil").which(player):
                subprocess.run(
                    [player, "-nodisp", "-autoexit", path] if player == "ffplay"
                    else [player, path],
                    check=False,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                return
        raise RuntimeError("No MP3 player found on this system.")
