from datetime import datetime

def run():

    now = datetime.now()

    return now.strftime(
        "Hôm nay là %d/%m/%Y"
    )
