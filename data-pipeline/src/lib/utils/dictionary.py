def rename(dictionary: dict, old_name, new_name):
    copy = dictionary.copy()
    copy[new_name] = copy[old_name]
    del copy[old_name]
    return copy

