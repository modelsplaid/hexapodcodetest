from hexapod.models import VirtualHexapod
from hexapod.plotter import HexapodPlotter
import json
from hexapod.ik_solver.ik_solver2 import inverse_kinematics_update
zero_pose = {
            0: {"coxia": 0, "femur": 0, "tibia": 0, "name": "right-middle", "id": 0},
            1: {"coxia": 0, "femur": 0, "tibia": 0, "name": "right-front", "id": 1},
            2: {"coxia": 0, "femur": 0, "tibia": 0, "name": "left-front", "id": 2},
            3: {"coxia": 0, "femur": 0, "tibia": 0, "name": "left-middle", "id": 3},
            4: {"coxia": 0, "femur": 0, "tibia": 0, "name": "left-back", "id": 4},
            5: {"coxia": 0, "femur": 0, "tibia": 0, "name": "right-back", "id": 5}
            }

out_file = open("./config/robot_dim_config.json", "r")
config_json = json.load(out_file)
BASE_DIMENSIONS = (config_json['BASE_DIMENSIONS'])

ik_parameters = (config_json['BASE_IK_PARAMS'])
COXIA_AXES_CONFIG = (config_json['COXIA_AXES'])

hexapod = VirtualHexapod(BASE_DIMENSIONS,COXIA_AXES_CONFIG)
BASE_PLOTTER = HexapodPlotter()

print("---Running in inverse_kinematics_update")
poses, hexapod = inverse_kinematics_update(hexapod, ik_parameters)




