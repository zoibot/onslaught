
objects = None

def init(obj):
    global objects
    objects = obj

def find_objects(typ):
    return [object for object in objects if type(object) is typ]

