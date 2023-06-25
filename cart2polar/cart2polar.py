import numpy as np
from math import *


class Cart2Polar:

    __slots__ = ("rad2deg","deg2rad")

    def __init__(self):
        self.rad2deg = 180/pi
        self.deg2rad = pi/180

    def rot_z_axis(self,pt_xyz=[0,0,0],rot_deg=0):
        """
        Given a point in cartesian coordinate, rotate this point along z-axis. 
        Return a rotated point in cartesian coordinate
        """
        roted_xyz = [0,0,0]
        roted_xyz[2] = pt_xyz[2] 
        rot_rad = rot_deg * self.deg2rad

        npt = np.array(pt_xyz)

        pt_len = np.sqrt(sum(npt*npt)) # Get lentgh of polar coord

        init_rad = atan2(pt_xyz[1],pt_xyz[0]) # Get initial angle of polar coord
        
        # New pos
        new_rad = init_rad + rot_rad

        new_x = cos(new_rad)*pt_len
        new_y = sin(new_rad)*pt_len

        roted_xyz[0] = new_x
        roted_xyz[1] = new_y
        return roted_xyz

def test1():
    cp = Cart2Polar()

    pt1 = [1,1,0]
    pt2 = cp.rot_z_axis(pt1,rot_deg=0)
    print("pt1: "+str(pt1)+" pt2: "+str(pt2) )

    pt1 = [-1,1,0]
    pt2 = cp.rot_z_axis(pt1,rot_deg=0)
    print("pt1: "+str(pt1)+" pt2: "+str(pt2) )

    pt1 = [-1,-1,0]
    pt2 = cp.rot_z_axis(pt1,rot_deg=0)
    print("pt1: "+str(pt1)+" pt2: "+str(pt2) )


    pt1 = [1,-1,0]
    pt2 = cp.rot_z_axis(pt1,rot_deg=0)
    print("pt1: "+str(pt1)+" pt2: "+str(pt2) )

def test2():
    cp = Cart2Polar()

    pt1 = [1,1,0]
    pt2 = cp.rot_z_axis(pt1,rot_deg=0)
    print("pt1: "+str(pt1)+" pt2: "+str(pt2) )

    pt1 = [1,1,0]
    pt2 = cp.rot_z_axis(pt1,rot_deg=45)
    print("pt1: "+str(pt1)+" pt2: "+str(pt2) )
        
    pt1 = [-1,1,0]
    pt2 = cp.rot_z_axis(pt1,rot_deg=44)
    print("pt1: "+str(pt1)+" pt2: "+str(pt2) )

    pt1 = [-1,-1,0]
    pt2 = cp.rot_z_axis(pt1,rot_deg=45)
    print("pt1: "+str(pt1)+" pt2: "+str(pt2) )

    pt1 = [1,-1,0]
    pt2 = cp.rot_z_axis(pt1,rot_deg=44)
    print("pt1: "+str(pt1)+" pt2: "+str(pt2) )

if __name__ == "__main__":
    test2()