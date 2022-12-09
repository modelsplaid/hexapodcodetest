import sys
sys.path.append("../../")

from copy import deepcopy
from hexapod.const import BASE_DIMENSIONS
from hexapod.models import VirtualHexapod
from hexapod.points import Vector
from hexapod.ik_solver import ik_solver, ik_solver2
from hexapod.ik_solver.shared import update_hexapod_points


def solveHexapodParams(dimensions, rawIKparams, rotateThenShift = True):
    hexapod = VirtualHexapod(dimensions)
    ikSolver_poses, _ = ik_solver2.inverse_kinematics_update(hexapod, rawIKparams)
    
    return    ikSolver_poses

if __name__ == '__main__':
    dimensions = {  # todo here
        "front": 100,
        "side": 100,
        "middle": 100,
        "coxia": 100,
        "femur": 100,
        "tibia": 100,
    }

    given_ik_parameters = {
        "hip_stance": 25,
        "leg_stance": 0,
        "percent_x": 0,
        "percent_y": 0,
        "percent_z": 0,
        "rot_x": 0,
        "rot_y": 0,
        "rot_z": 0,
    }


    ikSolver_poses = solveHexapodParams(dimensions, given_ik_parameters)
    print("ikSolver_poses:")
    print(ikSolver_poses)