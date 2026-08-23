import os

from services.base_service import BaseService


class SystemService(BaseService):

    def start(self):
        pass

    def stop(self):
        pass

    def shutdown(self):

        os.system(

            "shutdown /s /t 0"

        )

    def restart(self):

        os.system(

            "shutdown /r /t 0"

        )