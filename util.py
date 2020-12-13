
def id_maker(dict_id):
    if len(dict_id) == 0:
        ide = 1
    else:
        max_key = max(dict_id, key=int)
        ide = max_key + 1
    return int(ide)

