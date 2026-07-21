from datetime import datetime

def run():

    now = datetime.now()

    return now.strftime(
        "Bây giờ là %H giờ %M phút."
    )