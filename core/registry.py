from skills.open_notepad import run as open_notepad
from skills.open_calc import run as open_calc
from skills.open_google import run as open_google
from skills.open_youtube import run as open_youtube
from skills.time_now import run as now
from skills.date_today import run as today

COMMANDS = {
    "mấy giờ": now,
    "giờ": now,
    "hôm nay": today,
    "ngày": today,
    "notepad": open_notepad,
    "máy tính": open_calc,
    "calc": open_calc,
    "google": open_google,
    "youtube": open_youtube,
}