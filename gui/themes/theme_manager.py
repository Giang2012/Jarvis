from enum import Enum

class AIMode(Enum):

    NORMAL = "normal"

    STUDY = "study"

    PROGRAMMING = "programming"

    GAMING = "gaming"

    MOVIE = "movie"

    MUSIC = "music"

    NIGHT = "night"

    SLEEP = "sleep"

THEMES = {

        AIMode.NORMAL: {

            "background": "#10131A",

            "primary": "#00D8FF",

            "secondary": "#0099CC",

            "glow": "#00E5FF",

            "speed": 1.0

        },

        AIMode.STUDY: {

            "background": "#131722",

            "primary": "#7FE8FF",

            "secondary": "#3AB6D6",

            "glow": "#B8FFFF",

            "speed": 0.6

        },

        AIMode.PROGRAMMING: {

            "background": "#050505",

            "primary": "#00F5FF",

            "secondary": "#00A7C8",

            "glow": "#00FFFF",

            "speed": 1.5

        },

        AIMode.GAMING: {

            "background": "#090909",

            "primary": "#FF3D3D",

            "secondary": "#FF9900",

            "glow": "#FF5050",

            "speed": 2.5

        }

    }