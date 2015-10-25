class Component(object):
    def __init__(self, prefix=''):
        self.prefix = prefix

    def attach(self, entity):
        self.entity = entity

    def detach(self, entity):
        self.entity = None

    def update(self, entity):
        pass

    def get(self, key):
        return self.entity.bag[self.prefix + key]
