from hexapod.linkage import Linkage
from hexapod.models import Hexagon
import json
from copy import deepcopy


if __name__ == "__main__":

    out_file = open("./config/robot_dim_config.json", "r")
    config_json = json.load(out_file)
    BASE_DIMENSIONS = (config_json['BASE_DIMENSIONS'])
    coxia_axis_config = COXIA_AXES_CONFIG = (config_json['COXIA_AXES'])

    # for right middle linkage
    coxia = BASE_DIMENSIONS["coxia"]  #45.0
    femur = BASE_DIMENSIONS["femur"]  #75.0
    tibia = BASE_DIMENSIONS["tibia"]  #150.0
    front = BASE_DIMENSIONS["front"]  #59
    mid =   BASE_DIMENSIONS["middle"] #93
    side =  BASE_DIMENSIONS["side"]   #119
    
    # Parse robot mass
    MASSES = config_json["MASSES"]
        
    COXIA_AXES = coxia_axis_config

    chosen_leg_id = 0

    body = Hexagon(front, mid, side,coxia_axis_config)

    leg_rm = Linkage(
              coxia,
              femur,
              tibia,
              coxia_axis = body.COXIA_AXES[chosen_leg_id],
              new_origin = body.vertices[chosen_leg_id],
              name = body.VERTEX_NAMES[chosen_leg_id],
              id_number = 0,
              masses=MASSES
            )

    leg_rm.change_pose(10,20,30) # coxia, femur, tibia in deg
    print("---------mithi method:  ")
    print("body_contact: "+str(leg_rm.body_contact()))
    print("coxia_point: "+str(leg_rm.coxia_point()))
    print("femur_point: "+str(leg_rm.femur_point()))
    print("foot_tip: "+str(leg_rm.foot_tip()))

    print("---------mdh method:  ")
    leg_rm_mdh = deepcopy(leg_rm)
    leg_rm_mdh.change_pose_mdh(10,20,30.3) # coxia, femur, tibia in deg
    print("body_contact: "+str(leg_rm_mdh.body_contact()))
    print("coxia_point: "+str(leg_rm_mdh.coxia_point()))
    print("femur_point: "+str(leg_rm_mdh.femur_point()))
    print("foot_tip: "+str(leg_rm_mdh.foot_tip()))
    
