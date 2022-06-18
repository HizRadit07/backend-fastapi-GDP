def remove_none_data(dict:dict):
    new_dict = {key:val for key, val in dict.items() if val != None}
    return new_dict

def check_null_value_exist(dict:dict):
    for (key, val) in dict.items():
        if val == None:
            return True
    return False