class ServiceManager:

    def __init__(self):

        self.services = {}

    def register(self, name, service):

        self.services[name] = service

    def unregister(self, name):

        if name in self.services:

            del self.services[name]

    def exists(self, name):

        return name in self.services

    def get(self, name):

        return self.services.get(name)

    def all(self):

        return self.services
    def start_all(self):

        for service in self.services.values():

            if hasattr(service, "start"):

                service.start()
    def stop_all(self):

        for service in self.services.values():

            if hasattr(service, "stop"):

                service.stop()