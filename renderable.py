from component import Component
import gfx

class Renderable(Component):
    type = 'renderable'
    def __init__(self, lines, prefix=''):
        super(Renderable, self).__init__(prefix)
        self.gfx_id = gfx.create_object(lines)
        self.entity = None

    def attach(self, entity):
        self.entity = entity
        gfx.show_object(self.gfx_id, True)

    def detach(self, entity):
        self.entity = None
        gfx.destroy_object(self.gfx_id)

    def update(self, entity):
        pos = entity.bag[self.prefix + 'x'], entity.bag[self.prefix + 'y']
        angle = entity.bag[self.prefix + 'angle']
        gfx.set_transform(self.gfx_id, pos, angle)
        # TODO should be based on entity property
        gfx.show_object(self.gfx_id, True)

    def is_attached(self):
        return self.entity is not None

