import json 
import copy

NUTURAL_POSES_PULSE = {
0: {"coxia": 1971, "femur": 2017, "tibia": 1068, "name": "right-middle", "id": 0},
1: {"coxia": 2088, "femur": 2070, "tibia": 940, "name": "right-front", "id": 1},
2: {"coxia": 1908, "femur": 1989, "tibia": 3158, "name": "left-front", "id": 2},
3: {"coxia": 2056, "femur": 2081, "tibia": 3172, "name": "left-middle", "id": 3},
4: {"coxia": 2059, "femur": 2042, "tibia": 3181, "name": "left-back", "id": 4},
5: {"coxia": 2054, "femur": 1887, "tibia": 914, "name": "right-back", "id": 5},
}


NUTURAL_POSES_DEG = {
0: {"coxia": 0, "femur": 0, "tibia": 0, "name": "right-middle", "id": 0},
1: {"coxia": 0, "femur": 0, "tibia": 0, "name": "right-front", "id": 1},
2: {"coxia": 0, "femur": 0, "tibia": 0, "name": "left-front", "id": 2},
3: {"coxia": 0, "femur": 0, "tibia": 0, "name": "left-middle", "id": 3},
4: {"coxia": 0, "femur": 0, "tibia": 0, "name": "left-back", "id": 4},
5: {"coxia": 0, "femur": 0, "tibia": 0, "name": "right-back", "id": 5},
}


# If servo rotation direction same as model joint angle, set 1
# if opposite set -1.   
DIRECTION_POSES_PULSE = {
0: {"coxia": -1, "femur": -1, "tibia": 1, "name": "right-middle", "id": 0},
1: {"coxia": -1, "femur": -1, "tibia": 1, "name": "right-front", "id": 1},
2: {"coxia": -1, "femur": 1, "tibia": -1, "name": "left-front", "id": 2},
3: {"coxia": -1, "femur": 1, "tibia": -1, "name": "left-middle", "id": 3},
4: {"coxia": -1, "femur": 1, "tibia": -1, "name": "left-back", "id": 4},
5: {"coxia": -1, "femur": -1, "tibia": 1, "name": "right-back", "id": 5},
}

# joint of our hexa model has different  ids with the real-world servo 
# each entry stands for corresponding servo id
SERVO_ID_MAPPING = {    
0: {"coxia": 13, "femur": 14, "tibia": 15, "name": "right-middle", "id": 0},
1: {"coxia": 16, "femur": 17, "tibia": 18, "name": "right-front", "id": 1},
2: {"coxia": 7, "femur": 8, "tibia": 9, "name": "left-front", "id": 2},
3: {"coxia": 4, "femur": 5, "tibia": 6, "name": "left-middle", "id": 3},
4: {"coxia": 1, "femur": 2, "tibia": 3, "name": "left-back", "id": 4},
5: {"coxia": 10, "femur": 11, "tibia": 12, "name": "right-back", "id": 5},
}
  
# the pulses will send to servo
PULSES2SERVOS = {    
0: {"coxia": 0, "femur": 0, "tibia": 0, "name": "right-middle", "id": 0},
1: {"coxia": 0, "femur": 0, "tibia": 0, "name": "right-front", "id": 1},
2: {"coxia": 0, "femur": 0, "tibia": 0, "name": "left-front", "id": 2},
3: {"coxia": 0, "femur": 0, "tibia": 0, "name": "left-middle", "id": 3},
4: {"coxia": 0, "femur": 0, "tibia": 0, "name": "left-back", "id": 4},
5: {"coxia": 0, "femur": 0, "tibia": 0, "name": "right-back", "id": 5},
}


def dump_json():
    dict_json = {'NUTURAL_POSES_PULSE': NUTURAL_POSES_PULSE,\
            'NUTURAL_POSES_DEG': NUTURAL_POSES_DEG,\
            'DIRECTION_POSES_PULSE': DIRECTION_POSES_PULSE,\
            'SERVO_ID_MAPPING':SERVO_ID_MAPPING,
            'PULSES2SERVOS':PULSES2SERVOS      
            }
    out_file = open("const_hardware_config.json", "w") 
    json.dump(dict_json,out_file,indent = 4) 
    print("IN const hardware:  ")
    #print(NUTURAL_POSES_PULSE)    

def str_key2int(str_key_dic):
    int_key_dic = dict()
    for strkey in str_key_dic:
        int_key_dic[int(strkey)] = str_key_dic[strkey]
    return int_key_dic

def load_json():
    out_file = open("const_hardware_config.json", "r") 
    config_json = json.load(out_file)    
    strkeyNUTURAL_POSES_DEG = config_json['NUTURAL_POSES_DEG']
    strkeyNUTURAL_POSES_PULSE = config_json['NUTURAL_POSES_PULSE']
    strkeyDIRECTION_POSES_PULSE = config_json['DIRECTION_POSES_PULSE']
    strkeySERVO_ID_MAPPING = config_json['SERVO_ID_MAPPING']
    strkeyPULSES2SERVOS = config_json['PULSES2SERVOS']
    
    PULSES2SERVOS = str_key2int(strkeyPULSES2SERVOS)
    NUTURAL_POSES_DEG = str_key2int(strkeyNUTURAL_POSES_DEG)
    NUTURAL_POSES_PULSE = str_key2int(strkeyNUTURAL_POSES_PULSE) 
    DIRECTION_POSES_PULSE = str_key2int(strkeyDIRECTION_POSES_PULSE)
    SERVO_ID_MAPPING = str_key2int(strkeySERVO_ID_MAPPING)
    

    print('---PULSES2SERVOS')
    print(PULSES2SERVOS)
    print('---NUTURAL_POSES_DEG')
    print(NUTURAL_POSES_DEG)
    print('---NUTURAL_POSES_PULSE')
    print(NUTURAL_POSES_PULSE)
    print('---DIRECTION_POSES_PULSE')
    print(DIRECTION_POSES_PULSE)
    print('---SERVO_ID_MAPPING')
    print(SERVO_ID_MAPPING)
    #print('NUTURAL_POSES_DEG')
    #print(NUTURAL_POSES_DEG)    

if __name__ == "__main__":

        load_json()