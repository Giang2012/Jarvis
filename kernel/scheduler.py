import time
import threading


class Scheduler:

    def every(self, seconds, func):

        def loop():

            while True:

                time.sleep(seconds)

                func()

        threading.Thread(

            target=loop,

            daemon=True

        ).start()