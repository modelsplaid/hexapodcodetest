"""
@author: Luis Fernando Lara Tobar
@author: Peter Corke
@author: Samuel Drew
"""

from roboticstoolbox import DHRobot, RevoluteMDH
import numpy as np
import spatialmath.base as base
import time
from math import *
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

    def __init__(self, symbolic=False):

        if symbolic:
            

            zero = sym.zero()
            pi = sym.pi()
            a1, a2 = sym.symbol("a1 a2")  # type: ignore
            a0 = zero
        else:
            from math import pi

            zero = 0.0
            a0 = zero 
            a1 = 1.5
            a2 = 1.2

        L = [RevoluteMDH(a=a0, alpha=zero), RevoluteMDH(a=a1, alpha=zero),RevoluteMDH(a=a2, alpha=zero)]

        super().__init__(L, name="Planar 2 link", keywords=("planar",))

        self.qr = np.array([0, pi / 2,0])
        self.qz = np.zeros(3)

        self.addconfiguration("qr", self.qr)
        self.addconfiguration("qz", self.qz)

        self.addconfiguration_attr("q1", np.array([0, pi / 2,0]))
        self.addconfiguration_attr("q2", np.array([pi / 2, -pi / 2,0]))

        theta1,theta2, theta3 = base.sym.symbol('ϴ1,ϴ2, ϴ3')
        
        lk1sym=L[0].A(q=theta1)
        lk2sym=L[1].A(q=theta2)
        lk3sym=L[2].A(q=sym.zero())
        
        print("0_1_T: \n"+str(lk1sym))
        print("1_2_T: \n"+str(lk2sym))
        print("2_3_T: \n"+str(lk3sym))

        #print("1_2_T: \n"+str(lk1num))
        #print("2_3_T: \n"+str(lk2num))


def numerical_jacob():
    robot = Planar2(symbolic=False)
    
    print(robot)
    '''
    print("robot.fkine: \n"+str(robot.fkine([pi/4,pi/4])))
    print("robot.jacobe: \n"+str(robot.jacobe([pi/4,pi/4])))
    print("robot.jacob0: \n"+str(robot.jacob0([pi/4,pi/4])))
    '''
    #robot.plot([pi/4,pi/4],eeframe=True,jointaxes=True)
    #time.sleep(10)
    
def symbolic_jacob():
    import spatialmath.base.symbolic as sym

    zero = sym.zero()
    pi = sym.pi()
    theta1, theta2 = base.sym.symbol('ϴ1, ϴ2')
      
    robot = Planar2(symbolic=True)
    print(robot)
    
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

    symbolic_jacob()
    #numerical_jacob()
	      
