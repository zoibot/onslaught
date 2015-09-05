class Entity(object):
    components = []
    bag = {}

    def __init__(self, objects):
        objects.append(self)
        self.objects = objects

    def attach_component(self, component):
        component.attach(self)
        self.components.append(component)

    def get_component(self, type):
        for component in self.components:
            if component.type == type:
                return component
        return None

    def has_component(self, type):
        return self.get_component(type) != None

    def modify_bag_key(self, key, fn):
        def modify_key(entity):
            self.bag[key] = fn(self.bag[key])
        return modify_key

    def modify_bag(self, fn):
        def modify(entity):
            self.bag = fn(self.bag)
        return modify

    def update(self):
        for component in self.components:
            component.update(self)

    def spawn_object(self, entity):
        self.objects.append(entity)
