import subprocess

from services.base_service import BaseService


class AppService(BaseService):

    def start(self):

        return True

    def stop(self):

        return True

    def open(self, command):

        try:

            subprocess.Popen(
                command,
                shell=True
            )

            return True

        except Exception as e:

            print(
                "AppService error:",
                e
            )

            return False