import os
import platform
import subprocess
import time

try:
    import psutil
except Exception:
    psutil = None


class SystemService:
    def start(self):
        return True

    def stop(self):
        return True

    def status(self):
        result = {
            "platform": platform.platform(),
            "python": platform.python_version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
        }
        if psutil:
            result.update({
                "cpu_percent": psutil.cpu_percent(interval=0.2),
                "memory_percent": psutil.virtual_memory().percent,
                "memory_used_gb": round(psutil.virtual_memory().used / 1024**3, 2),
                "memory_total_gb": round(psutil.virtual_memory().total / 1024**3, 2),
                "uptime_hours": round(
                    (time.time() - psutil.boot_time()) / 3600, 1
                ),
            })
        return result

    def execute_safe(self, action):
        action = str(action or "").lower()
        if "restart" in action or "khởi động lại" in action:
            return "REQUIRES_CONFIRMATION: restart"
        if "shutdown" in action or "tắt máy" in action:
            return "REQUIRES_CONFIRMATION: shutdown"
        if "lock" in action or "khóa" in action:
            return "REQUIRES_CONFIRMATION: lock"
        return "Unknown system action."

    def confirm_and_execute(self, action):
        action = str(action or "").lower()
        if "restart" in action or "khởi động lại" in action:
            subprocess.run(["shutdown", "/r", "/t", "0"], check=False)
            return "Restart requested."
        if "shutdown" in action or "tắt máy" in action:
            subprocess.run(["shutdown", "/s", "/t", "0"], check=False)
            return "Shutdown requested."
        if "lock" in action or "khóa" in action:
            subprocess.run(["rundll32.exe", "user32.dll,LockWorkStation"], check=False)
            return "Lock requested."
        return "Unknown system action."
