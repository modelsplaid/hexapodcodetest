#!/usr/bin/env python

import numpy as np
from roboticstoolbox.robot.ET import ET
from roboticstoolbox.robot.ETS import ETS
from roboticstoolbox.robot.ERobot import ERobot
from roboticstoolbox.robot.Link import Link
from math import *
import time
import roboticstoolbox as rtb
from spatialmath import SE3
class EHexaLeg(ERobot):

    def __init__(self):
        front = 0.059
        side = 0.119
        middle = 0.093
        coxia = 0.045
        femur = 0.075
        tibia = 0.140
        
        # robot centrual base
        robot_base = Link(ET.Rz(), name="robot_base", jindex=0, parent=None)

        
        # right middle
        rm_base = Link(ET.tx(middle)*ET.Rz(), name="rm_base", jindex=1, parent=robot_base)
        rm_coxia = Link(ET.tx(coxia)*ET.Rx(pi/2)*ET.Rz() , name="rm_coxia", jindex=2, parent=rm_base)
        rm_femur = Link(ET.tx(femur)*ET.Rz(), name="rm_femur", jindex=3, parent=rm_coxia)
        rm_tibia = Link(ETS(ET.tx(tibia)), name="rm_tibia", parent=rm_femur)
        rm_leg = [rm_base, rm_coxia,rm_femur,rm_tibia] 

        # right front 
        rf_base = Link(ET.tx(front)*ET.ty(side)*ET.Rz(), name="rf_base", jindex=4, parent=robot_base)
        rf_coxia = Link(ET.tx(coxia)*ET.Rx(pi/2)*ET.Rz() , name="rf_coxia", jindex=5, parent=rf_base)
        rf_femur = Link(ET.tx(femur)*ET.Rz(), name="rf_femur", jindex=6, parent=rf_coxia)
        rf_tibia = Link(ETS(ET.tx(tibia)), name="rf_tibia", parent=rf_femur)
        rf_leg = [rf_base, rf_coxia,rf_femur,rf_tibia] 

        # right back
        rb_base = Link(ET.tx(front)*ET.ty(-side)*ET.Rz(), name="rb_base", jindex=7, parent=robot_base)
        rb_coxia = Link(ET.tx(coxia)*ET.Rx(pi/2)*ET.Rz() , name="rb_coxia", jindex=8, parent=rb_base)
        rb_femur = Link(ET.tx(femur)*ET.Rz(), name="rb_femur", jindex=9, parent=rb_coxia)
        rb_tibia = Link(ETS(ET.tx(tibia)), name="rb_tibia", parent=rb_femur)
        rb_leg = [rb_base, rb_coxia,rb_femur,rb_tibia] 


        

        elinks = [robot_base]+rf_leg+rm_leg+rb_leg
        #elinks = [robot_base]+rf_leg#rm_leg

        super().__init__(elinks, name="EHexaLeg")

        self.qr = np.array([0,0,0,0,0,0,0,0,0,0])
        self.qz = np.zeros(10)

        self.addconfiguration("qr", self.qr)
        self.addconfiguration("qz", self.qz)


def testjtraj():
    deg = pi / 180
    qs = np.array([10.1, -19.3, -29.6]) * deg
    qt = np.array([15.1, 10.3, -20.6]) * deg

    traj = rtb.jtraj(qs, qt, 10)
    #print("robotraj arrive: \n"+str(traj.arrive ))
    print("robotraj info: \n"+str(traj.t))
    print("robotraj via: \n"+str(traj.s ))

    hexaleg = EHexaLeg()
    print(hexaleg)
    #hexaleg.plot(traj.s,eeframe=True,jointaxes=True)


def testinv():
    deg = pi / 180

    hexaleg = EHexaLeg()
    print(hexaleg)

    # init location 
    qr = np.array([10.1, -19.3, -29.6]) * deg

    # target location 
    qt = np.array([10.7, -20.7, -30.7],dtype='float64') * deg

    # targe matrix
    mat_target = hexaleg.fkine(qt)
    print("mat_target: \n"+str(mat_target))

    T = SE3(0.199,0.0376,-0.1359)

    print("T: \n"+str(T) )
    # inverse kinematics
    #q_target = hexaleg.ikine_LM(T,mask=[1,1,1,0,0,0],q0=[10.7*deg,20.7*deg,30.7*deg])
    q_target = hexaleg.ikine_LM(T,mask=[1,1,1,0,0,0],q0=qr)

    print("q_target:"+str(q_target) )
    print(q_target[0]/deg)

    mat_estimated = hexaleg.fkine(q_target[0])
    print("mat_estimated: \n"+str( mat_estimated))

    #hexaleg.plot(q_target[0])
    #time.sleep(10)
    return mat_target

if __name__ == "__main__":  # pragma nocover
    hexaleg = EHexaLeg()
    mat_target = hexaleg.fkine_all(hexaleg.qr)
    print("mat_target: \n"+str(mat_target))
    print(hexaleg)
    #while True:
    hexaleg.plot(hexaleg.qr) 
    time.sleep(10)
