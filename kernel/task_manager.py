import queue
import threading


class TaskManager:

    def __init__(self):

        self.tasks = queue.Queue()

        threading.Thread(

            target=self.worker,

            daemon=True

        ).start()

    def add(self, func, *args):

        self.tasks.put(

            (func, args)

        )

    def worker(self):

        while True:

            func, args = self.tasks.get()

            func(*args)

            self.tasks.task_done()