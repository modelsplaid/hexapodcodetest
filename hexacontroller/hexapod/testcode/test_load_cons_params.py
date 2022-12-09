import json
out_file = open("../../config/robot_dim_config.json", "r")
config_json = json.load(out_file)
BASE_DIMENSIONS = (config_json['BASE_DIMENSIONS'])
BASE_IK_PARAMS = (config_json['BASE_IK_PARAMS'])
print(BASE_DIMENSIONS['front'] )
