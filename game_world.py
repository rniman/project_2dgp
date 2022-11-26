# layer 0: background
# layer 1: enemy
# layer 2: friendly
# layer 3: mainCharacter
game_object = [[], [], [], [], [], []]

#collision information
# key 'main:ladder' string
# value [ [main],[ladder1,ladder1,...]]
collision_group = dict()

def add_object(object, depth = 0):
    game_object[depth].append(object)

def add_objects(object_list, depth):
    game_object[depth] += object_list

def remove_object(object):
    for layer in game_object:
        try:
            layer.remove(object)
            remove_collision_object(object)
            del object
            return
        except:
            pass
    raise ValueError('Trying destroy non existing object')

def all_objects():
    for layer in game_object:
        for o in layer:
            yield o

def clear():
    for o in all_objects():
        del o
    for layer in game_object:
        layer.clear()
    for a, b, group in all_collision_pairs():
        del a, b, group
    collision_group.clear()


def add_collision_pairs(first, second, group):
    if group not in collision_group:
        collision_group[group] = [[], []]

    # a b의 None 확인 이유 b만 추가 할경우 add_c_p(None,b,name)을 쓸수 있기 때문
    if first:
        if type(first) == list:
            collision_group[group][0] += first
        else: # 단일 오브젝트
            collision_group[group][0].append(first)

    if second:
        if type(second) == list:
            collision_group[group][1] += second
        else: # 단일 오브젝트
            collision_group[group][1].append(second)

def all_collision_pairs():  # 제너레이터
    for group, pairs in collision_group.items():  # 딕셔너리의 키와 벨류를 가져옴
        for a in pairs[0]:
            for b in pairs[1]:
                yield a, b, group

def remove_collision_object(object):
    for pairs in collision_group.values():
        if object in pairs[0]: pairs[0].remove(object)
        elif object in pairs[1]: pairs[1].remove(object)

def init_collision_state(fir, sec, group):
    fir.init_collision(group)
    sec.init_collision(group)