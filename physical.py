from component import *

class Physical(Component):
    type = 'physical'
    def attach(self, entity):
        entity.bag['x'] = 0
        entity.bag['y'] = 0
        entity.bag['angle'] = 0
