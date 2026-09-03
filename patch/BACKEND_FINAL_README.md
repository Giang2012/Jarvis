# J.A.R.V.I.S Backend — Final Capability Layer

This patch upgrades the backend from a small command demo into a local-first
desktop assistant foundation.

## Capabilities

### Desktop
- Open applications
- Close applications
- Keyboard press / hotkeys
- Type text
- Mouse click / movement
- Screenshots
- File opening

### Screen awareness
- Local screenshot capture
- OCR with coordinates
- Find visible text
- Optional semantic screen description through a local Ollama vision model
- Optional polling observer
- Qt signal from Brain for GUI integration

Screen awareness is OFF by default. Enable explicitly with:

```python
brain.enable_screen_awareness()
```

Semantic vision requires a local Ollama vision model configured through:

```text
JARVIS_VISION_MODEL
```

Example:

```text
llava:7b
```

### Web / information
Existing BrowserService and SearchSkill remain the web entry point.

### System
- CPU/RAM/uptime status
- Restart/shutdown/lock are gated behind explicit confirmation
- No arbitrary shell text is executed by the planner

### Files
- List directories
- Search filenames
- Open files/folders

### Media
- Play/pause
- Next/previous
- Volume up/down
- Mute

### Clipboard
- Read clipboard
- Set clipboard

### Agent-style chaining
Examples:

```text
mở chrome rồi tìm black hole
mở notepad rồi nhập hello
chụp màn hình
nhìn màn hình xem tôi đang làm gì
```

The deterministic planner handles these actions before the natural-language
Ollama fallback.

## Dependencies

The existing project already contains PyAutoGUI/Pillow. Add:

```text
psutil
pytesseract
```

`pytesseract` also needs the Tesseract OCR executable installed on Windows
for OCR to be active. Without it, screenshot capture still works.

## Security model

The backend intentionally does NOT turn arbitrary LLM output into arbitrary
PowerShell/cmd execution. Destructive system operations require a separate
confirmation step. Screen observation is opt-in and local-first.

## Integration

Replace the corresponding files in:

```text
core/
ai/
services/
skills/
config/
tests/
```

Then run:

```powershell
python -m compileall core ai services skills config tests
python -m pytest tests/test_backend_capabilities.py
```

If pytest is not installed, run the compile command and the existing
`test_brain.py`.
