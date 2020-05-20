def define_order(old):
    new = []
    new_order = [0,1,5,4,6,7,3,2]
    for i, val in enumerate(new_order):
        new.append(old[val])
    return new