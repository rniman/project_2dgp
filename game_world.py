# layer 0: background
# layer 1: enemy
# layer 2: friendly
# layer 3: mainCharacter
game_object = [[], [], [], []]

def add_object(object, depth = 0):
    game_object[depth].append(object)

def add_objects(object_list, depth):
    game_object[depth] += object_list

def remove_object(object):
    for layer in game_object:
        if object in layer:
            layer.remove(object)
            del object
            return

def all_objects():
    for layer in game_object:
        for o in layer:
            yield o

def clear():
    for o in all_objects():
        del o
    for layer in game_object:
        layer.clear()