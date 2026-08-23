class ServiceManager:

    def __init__(self):

        self.services = {}

    def register(self, name, service):

        self.services[name] = service

    def get(self, name):

        return self.services.get(name)

    def start_all(self):

        for service in self.services.values():

            if hasattr(service, "start"):

                service.start()

    def stop_all(self):

        for service in self.services.values():

            if hasattr(service, "stop"):

                service.stop()

    def remove(self, name):

        if name in self.services:

            del self.services[name]

    def clear(self):

        self.services.clear()

    def list(self):

        return list(self.services.keys())