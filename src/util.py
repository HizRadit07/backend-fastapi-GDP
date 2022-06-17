def remove_none_data(dict:dict):
    new_dict = {key:val for key, val in dict.items() if val != None}
    return new_dict