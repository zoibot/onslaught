from component import *

class Physical(Component):
    type = 'physical'
    def attach(self, entity):
        super(Physical, self).attach(entity)
        entity.bag[self.prefix + 'x'] = 0
        entity.bag[self.prefix + 'y'] = 0
        entity.bag[self.prefix + 'angle'] = 0

    def update(self, entity):
        # what does this do?
        self.entity.bag[self.prefix + 'x'] = self.get('x')
        self.entity.bag[self.prefix + 'y'] = self.get('y')
        self.entity.bag[self.prefix + 'angle'] = self.get('angle')
