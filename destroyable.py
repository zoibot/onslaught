from component import *

destroyables = []

def get_destroyables():
    return destroyables

# singleton
class Destroyable(Component):
    type = 'destroyable'
    def __init__(self, shape = None, prefix = ''):
        self.shape = shape
        self.prefix = prefix

    def attach(self, entity):
        super(Destroyable, self).attach(entity)
        destroyables.append(self)

    def detach(self, entity):
        super(Destroyable, self).detach(entity)
        global destroyables
        print destroyables
        destroyables = [destroyable for destroyable in destroyables if destroyable != self]
        print destroyables
    
    def collides(self, x, y):
        ex, ey = self.get('x'), self.get('y')
        if self.shape:
            return self.shape.collides(ex, ey, x, y)
        else:
            return (ex - x)**2 + (ey - y)**2 < 25

    def destroy(self):
        self.entity.destroy()

    def update(self, entity):
        pass
