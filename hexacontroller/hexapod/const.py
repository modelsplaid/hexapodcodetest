from copy import deepcopy
from hexapod.plotter import HexapodPlotter
from hexapod.models import VirtualHexapod, Hexagon, Linkage
from hexapod.templates.figure_template import HEXAPOD_FIGURE
from hexapod.templates.pose_template import HEXAPOD_POSE
import sys
import json
sys.path.append("../../")

SIMULATOR_MODE = False
try: 
    from Hardware import jointangle_to_pulse
except Exception: 
    print("Warning Hardware not found. In simulation mode.")
    SIMULATOR_MODE = True

try:
    VIRTUAL_TO_REAL = \
        jointangle_to_pulse.VirtualToReal(\
            net_socket_config_file='config/net_commu_config.json',\
            servo_io_commu_template = "config/servo_io_commu.json",\
            const_hardware_config_file="./config/leg2servo_config.json"    
                )
except Exception as e: 
    print("VIRTUAL_TO_REAL variable will not be created. Error msg:")
    print(e)
    SIMULATOR_MODE = True
    #raise Exception
NAMES_LEG = Hexagon.VERTEX_NAMES
NAMES_JOINT = Linkage.POINT_NAMES


out_file = open("./config/robot_dim_config.json", "r")
config_json = json.load(out_file)
BASE_DIMENSIONS = (config_json['BASE_DIMENSIONS'])
BASE_IK_PARAMS = (config_json['BASE_IK_PARAMS'])
COXIA_AXES_CONFIG = (config_json['COXIA_AXES'])


print("instance BASE_POSE")
BASE_POSE = deepcopy(HEXAPOD_POSE)

print("instance VirtualHexapod")
BASE_HEXAPOD = VirtualHexapod(BASE_DIMENSIONS)
print("--------instance BASE_PLOTTER")
BASE_PLOTTER = HexapodPlotter()

HEXAPOD = deepcopy(BASE_HEXAPOD)
HEXAPOD.update(HEXAPOD_POSE)
BASE_FIGURE = deepcopy(HEXAPOD_FIGURE)
BASE_PLOTTER.update(BASE_FIGURE, HEXAPOD)
