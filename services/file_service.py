import os


class FileService:

    def exists(self, path):

        return os.path.exists(path)

    def open(self, path):

        os.startfile(path)