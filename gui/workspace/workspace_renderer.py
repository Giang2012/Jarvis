class WorkspaceRenderer:

    def render(self, painter, manager):

        objects = sorted(

            manager.objects,

            key=lambda o:

            o.transform.depth

        )

        for obj in objects:

            obj.render(painter)