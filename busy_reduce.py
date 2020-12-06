import json 

CUT_OFF_VALUE = 2727.75748502994 + 1154.7228889082112


if __name__ == '__main__':
    day_vals = None 

    with open("busiest_days_asc.json", "r") as fr:
        day_vals = json.loads(fr.read())

    
    new_list: list = []


    for val in day_vals:
        if val[1] >= CUT_OFF_VALUE:
            new_list.append(val[0]) 

    with open("busiest_days_asc_reduced.json", "w") as fw:
        json.dump(new_list, fw)
