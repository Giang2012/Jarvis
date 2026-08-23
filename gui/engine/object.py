from gui.engine.transform import Transform
from gui.engine.component_manager import ComponentManager


class Object:

    def __init__(self):

        self.name = ""

        self.transform = Transform()

        self.components = ComponentManager()

    # ----------------------------

    def addComponent(self, component):

        self.components.add(

            component,

            self

        )

    # ----------------------------

    def update(self):

        self.components.update()

    # ----------------------------

    def render(self, painter):

        painter.save()

        painter.translate(

            self.transform.position

        )

        painter.rotate(

            self.transform.rotation

        )

        painter.scale(

            self.transform.scale,

            self.transform.scale

        )

        painter.setOpacity(

            self.transform.opacity

        )

        self.components.render(

            painter

        )

        painter.restore()
    def getComponent(self, componentType):

        return self.components.get(componentType)


    def removeComponent(self, componentType):

        self.components.remove(componentType)