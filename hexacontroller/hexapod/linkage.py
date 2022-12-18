#
#--------------     
# Dimensions of 
# f, s, and m
#--------------     
#                              |-f-|
#                              *---*---*--------
#                             /   y^    \     |
#                            /     |     \    s
#                           /      |      \   |
#                          *------cog--->--* ---
#                           \      |    x /|
#                            \     |     / |
#                             \    |    /  |
#                              *---*---*   |
#                                  |       |
#                                  |---m---|
#                        
#                                  y axis
#                                  ^
#                                  |
#                                  |
#                                  ----> x axis
#                                cog (origin)
#
#--------------                                
#Top-down view
#--------------
#Note: legs' axis configuration is based on mdh. For mdh, only z-axis rotates.
# 
#                            x2          x1
#                             \         /
#                              *---*---*   
#    z3t^     z3f^            /    |    \  ^y0c     
#       |        |           /     |     \ |         
#       |        |   coxia  /      |      \|         femur    tibia
# x3t<---  x3f<---  x3c----*------cog------*---->x0c ----x0f  ----z0t     
#  tibia    femur          |\      |      /coxia     |        |
#                          | \     |     /           |        |
#                       y3c|  \    |    /            |z0f     |z0t
#                              *---*---*
#                             /         \
#                            x4         x5  
# -------------
# LINKAGE
# -------------
# Linkage is defined in MDH(modified denavit hartenberg) format
# Zero joint position of the linkages (alpha=0, beta=0, gamma=0) is defined as below:
#  link b and link c form a straight line
#  link a and link b form a straight line
#  link a and the leg x-axis are aligned
#
# alpha - the angle linkage a makes with x_axis about z axis
# beta  - the angle that linkage a makes with linkage b
# gamma - the angle that linkage c make with the line perpendicular to linkage b
#
#
# MEASUREMENTS
#
#  |------a---------|--------b------|-------c----------|
#  |================|---------------|------------------|
#  p0               p1              p2                 p3
#                               
#  p0 - body contact (where joint0 alpha located)
#  p1 - coxia point  (where joint1 beta located)
#  p2 - femur point  (where joint2 gamma located)
#  p3 - foot tip     (where tip coordinate located)
#
#  z    /y           y               y                  y          
#  |   /             |               |                  |          
#  |  /              |               |                  |            
#  | /               |               |                  |           
#  |/                |               |                  |           
#  /--------> x      /-------> x     /-------> x        /-------> x      
#                   /               /                  /            
#                  /               /                  /             
#                 /               /                  /              
#                z               z                  z               
#   
#   joint0         joint1        joint2             tip coordinate 
#    alpha          beta          gamma 
#
#
#
#
# ---------------------------
# ANGLES alpha beta and gamma
# ---------------------------
#
#    ---TOP TO DOWM VIEW---
#
#  body    *-----*------  
#  |      / femur  tibia
#  |     /   (b)    (c)
#  |    / 
#  |   /
#  |  / coxia
#  | /   (a)
#  |/
#  * 
#  alpha 
#                
#    ---BACK TO FROM VIEW---
#           
#          ---- /* ---------
#         /    //\\        \
#        b    //  \\        \
#       /    //    \\        c
#      /    //beta  \\        \
#  *=======* ---->   \\        \
#  |---a---|          \\        \
#                     *-----------
#
#    ---BACK TO FROM VIEW---
#    
# |--a--|---b----|
# *=====*=========* -------------
#               | \\            \
#               |  \\            \
#               |   \\            c
#               |    \\            \
#               |gamma\\            \
#               |      *----------------
#
#
#Joint direction definition: 
#For joint beta and gamma: positive: move up.       negative: move down.
#For right side alpha    : positive: move forward.  negative: move backward.
#For left side alpha     : positive: move backward. negative: move forward.

from copy import deepcopy
import numpy as np
from hexapod.points import (
    Vector,
    frame_yrotate_xtranslate,
    frame_zrotate_xytranslate,
)

from hexapod.hexaMDH_jacob import HexaLeg

class Linkage:
    POINT_NAMES = ["coxia", "femur", "tibia"]

    __slots__ = (
        "a",
        "b",
        "c",
        "alpha",
        "beta",
        "gamma",
        "coxia_axis",
        "new_origin",
        "name",
        "id",
        "all_points",
        "ground_contact_point",
        "masses",
        "mm_to_m",
        "mdhleg"
    )

    def __init__(self,a,b,c,alpha=0,beta=0,gamma=0,
            coxia_axis=0,new_origin=Vector(0, 0, 0),name=None,
            id_number=None,masses=None):
        # a,b,c: lenght in mm 
        # alpha,beta,gamma,coxia_axis: in deg
        
        
        self.a = a # coxia length 
        self.b = b # femur length
        self.c = c # tibia length
        self.new_origin = new_origin
        self.coxia_axis = coxia_axis
        self.id = id_number
        self.name = name
        self.masses = masses
        
        m1_kg = self.masses["m1"]
        m2_kg = self.masses["m2"]
        m3_kg = self.masses["m3"]
        m4_kg = self.masses["m4"]
        
        self.mm_to_m = 1.0/1000.0
        
        # Object right-middle leg 
        self.mdhleg = HexaLeg(False,a*self.mm_to_m,\
                b*self.mm_to_m,c*self.mm_to_m,
                m1_kg = m1_kg,
                m2_kg = m2_kg,
                m3_kg = m3_kg,
                m4_kg = m4_kg
                )
        
        self.mdhleg.fkine((0,0,0,0))
        
        self.change_pose_deg(alpha, beta, gamma)

    def coxia_angle(self):
        return self.alpha

    def body_contact(self):
        return self.all_points[0]

    def coxia_point(self):
        return self.all_points[1]

    def femur_point(self):
        return self.all_points[2]

    def foot_tip(self):
        return self.all_points[3]

    def ground_contact(self):
        return self.ground_contact_point

    def get_point(self, i):
        return self.all_points[i]

    def change_pose_mdh_deg(self, alpha, beta, gamma):
        pass 
    
    def change_pose_deg(self, alpha, beta, gamma):
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma

        # frame_ab is the pose of frame_b wrt frame_a
        frame_01 = frame_yrotate_xtranslate(theta=-self.beta, x=self.a)
        frame_12 = frame_yrotate_xtranslate(theta=self.gamma, x=self.b)
        frame_23 = frame_yrotate_xtranslate(theta=0, x=self.c)

        frame_02 = np.matmul(frame_01, frame_12)
        frame_03 = np.matmul(frame_02, frame_23)
        
        # tzq print new frame
   
        new_frame = frame_zrotate_xytranslate(
            self.coxia_axis + self.alpha, self.new_origin.x, self.new_origin.y
        )

        # find points wrt to body contact point
        p0 = Vector(0, 0, 0)
        p1 = p0.get_point_wrt(frame_01)
        p2 = p0.get_point_wrt(frame_02)
        p3 = p0.get_point_wrt(frame_03)

        # find points wrt to center of gravity
        p0 = deepcopy(self.new_origin)
        p0.name += "-body-contact"
        p1 = p1.get_point_wrt(new_frame, name=self.name + "-coxia")
        p2 = p2.get_point_wrt(new_frame, name=self.name + "-femur")
        p3 = p3.get_point_wrt(new_frame, name=self.name + "-tibia")


        self.all_points = [p0, p1, p2, p3]
        self.ground_contact_point = self.compute_ground_contact()

    def update_leg_wrt(self, frame, height):
        for point in self.all_points:
            point.update_point_wrt(frame, height)

    def compute_ground_contact(self):
        # ❗IMPORTANT: Verify if this assumption is correct
        # ❗VERIFIED: This assumption is indeed wrong
        ground_contact = self.all_points[3]
        for point in reversed(self.all_points):
            if point.z < ground_contact.z:
                ground_contact = point

        return ground_contact

    def __str__(self):
        leg_string = f"{self!r}\n"
        leg_string += f"Vectors of {self.name} leg:\n"

        for point in self.all_points:
            leg_string += f"  {point}\n"

        leg_string += f"  ground contact: {self.ground_contact()}\n"
        return leg_string

    def __repr__(self):
        return f"""Linkage(
  a={self.a},
  b={self.b},
  c={self.c},
  alpha={self.alpha},
  beta={self.beta},
  gamma={self.gamma},
  coxia_axis={self.coxia_axis},
  id_number={self.id},
  name='{self.name}',
  new_origin={self.new_origin},
)"""



