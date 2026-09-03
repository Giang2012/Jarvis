import sys

from ai.reasoner import Reasoner


def check(text, expected):
    actions = [task.action for task in Reasoner().build(text)]
    print(f"{text!r} -> {actions}")
    if actions != expected:
        raise AssertionError((text, actions, expected))


def main():
    check("mở chrome rồi tìm black hole", ["OPEN_APP", "SEARCH"])
    check("nhìn màn hình xem tôi đang làm gì", ["VISION"])
    check("chụp màn hình", ["SCREENSHOT"])
    check("next track", ["MEDIA"])
    check("thời tiết", ["WEATHER"])
    print("BACKEND SMOKE TEST: PASS")


if __name__ == "__main__":
    main()
