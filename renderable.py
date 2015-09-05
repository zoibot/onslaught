from component import Component
import gfx

class Renderable(Component):
    type = 'renderable'
    def __init__(self, lines):
        self.gfx_id = gfx.create_object(lines)
        self.entity = None

    def attach(self, entity):
        self.entity = entity
        gfx.show_object(self.gfx_id, True)

    def update(self, entity):
        pos = entity.bag['x'], entity.bag['y']
        angle = entity.bag['angle']
        gfx.set_transform(self.gfx_id, pos, angle)
        # TODO should be based on entity property
        gfx.show_object(self.gfx_id, True)

    def is_attached(self):
        return self.entity is not None

