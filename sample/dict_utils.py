def search_index(dict_list, key, value):
    return dict_list.index(next(item for item in dict_list if item[key] == value))
