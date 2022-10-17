"""
@author: Luis Fernando Lara Tobar
@author: Peter Corke
@author: Samuel Drew
"""

from roboticstoolbox import DHRobot, RevoluteMDH
import numpy as np
import spatialmath.base as base
import time
#from math import *
from sympy import *
import spatialmath.base.symbolic as sym

class Planar2(DHRobot):
    """
    Class that models a planar 2-link robot

    ``Planar2()`` is a class which models a 2-link planar robot and
    describes its kinematic characteristics using standard DH
    conventions.

    .. runblock:: pycon

        >>> import roboticstoolbox as rtb
        >>> robot = rtb.models.DH.Planar2()
        >>> print(robot)

    Defined joint configurations are:

        - qz, zero angles, all folded up
        - q1, links are horizontal and vertical respectively
        - q2, links are vertical and horizontal respectively

    .. note::

      - Robot has only 2 DoF.

    .. codeauthor:: Peter Corke
    """

    def __init__(self, symbolic=True):


        zero = sym.zero()
        pi = sym.pi()
        a1, a2 = sym.symbol("l1 l2")  # type: ignore
        a0 = zero

        r0 = [a1, zero, zero] # center of mass position with respect to ith link
        r1 = [a2, zero, zero] # center of mass position with respect to ith link
        r2 = [zero, zero, zero] # center of mass position with respect to ith link

        m1, m2, = sym.symbol("m1 m2")  # type: ignore
        m3 = zero

        I1=[zero, zero, zero, zero, zero, zero]
        I2=[zero, zero, zero, zero, zero, zero]
        I3=[zero, zero, zero, zero, zero, zero]

        
        L = [\
            RevoluteMDH(a=a0, alpha=zero,r=r0,m=m1,I=I1,Jm=zero,G=zero,B=zero,Tc=[zero,zero]),\
            RevoluteMDH(a=a1, alpha=zero,r=r1,m=m2,I=I2,Jm=zero,G=zero,B=zero,Tc=[zero,zero]),\
            RevoluteMDH(a=a2, alpha=zero,r=r2,m=m3,I=I3,Jm=zero,G=zero,B=zero,Tc=[zero,zero])\
            ]

        super().__init__(L, symbolic=True,name="Planar 2 link", keywords=("planar",))

        self.qr = [pi/4, pi/4, pi/4]
        self.qz = [zero, zero, zero]

        self.addconfiguration("qr", self.qr)
        self.addconfiguration("qz", self.qz)

        theta1,theta2 = base.sym.symbol('ɵ1, ɵ2')
        
        lk1sym=L[0].A(q=theta1)
        lk2sym=L[1].A(q=theta2)
        lk3sym=L[2].A(q=sym.zero())
        
        print("0_1_T: \n"+str(lk1sym))
        print("1_2_T: \n"+str(lk2sym))
        print("2_3_T: \n"+str(lk3sym))

def symbolic_dyna():

    theta1,theta2 = base.sym.symbol('ɵ1, ɵ2')
    thetad1,thetad2 = base.sym.symbol('ɵ́1, ɵ́2')
    thetadd1,thetadd2 = base.sym.symbol('ɵ̋1, ɵ̋2')
    zero = sym.zero()
    pi = sym.pi()
    grav_g = base.sym.symbol('g')

    thetas = [theta1,theta2,zero]
    thetads = [thetad1,thetad2,zero]
    thetadds = [thetadd1,thetadd2,zero]
    gravs = [zero,grav_g,zero]


    robot = Planar2(symbolic=True)
    dynamat=robot.rne_python(Q=thetas,QD=thetads,QDD=thetadds,gravity=gravs)
    
    print("dynamat:\n")
    print(dynamat)
    simpdynamat = simplify(dynamat)

    print("simpdynamat:\n")
    for i in range(len(simpdynamat)):
        print(simpdynamat[i])
def symbolic_jacob():
    

    zero = sym.zero()
    pi = sym.pi()
    theta1, theta2 = base.sym.symbol('ɵ1, ɵ2')

      
    robot = Planar2(symbolic=True)
    print(robot)

    robot.rne_python()
    
    ## fkine 
    
    fkin = robot.fkine([theta1,theta2,zero])
    #sfkin = simplify(fkin)
    sfkin = fkin
    print("robot.fkine: \n"+str(sfkin))
    
    
    ## jacob end effector frame
    jacobe = robot.jacobe([theta1,theta2,zero])
    sjacobe = simplify(jacobe)
    print("robot.jacobe: \n"+str(sjacobe))
    
    ## jacob base frame
    jacob0 = robot.jacob0([theta1,theta2,zero])
    sjacob0 = simplify(jacob0)
    print("robot.jacob0: \n"+str(sjacob0))
    
    
    #robot.plot([pi/4,pi/4],eeframe=True,jointaxes=True)
    #time.sleep(10)
    

if __name__ == "__main__":  # pragma nocover
    symbolic_dyna()
    #symbolic_jacob()
	      
