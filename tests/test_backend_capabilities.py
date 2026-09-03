from ai.reasoner import Reasoner


def actions(text):
    return [task.action for task in Reasoner().build(text)]


def test_multi_step():
    assert actions("mở chrome rồi tìm black hole") == ["OPEN_APP", "SEARCH"]


def test_screen():
    assert actions("nhìn màn hình xem tôi đang làm gì") == ["VISION"]


def test_media():
    assert actions("next track") == ["MEDIA"]


def test_weather():
    assert actions("thời tiết") == ["WEATHER"]
