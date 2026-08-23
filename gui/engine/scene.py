class Scene:

    def __init__(self):

        self.objects = []

    def add(self, obj):

        self.objects.append(obj)

    def update(self):

        for obj in self.objects:

            obj.update()

    def render(self, painter):

        for obj in self.objects:

            obj.render(painter)