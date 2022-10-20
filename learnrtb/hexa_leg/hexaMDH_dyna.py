import numpy as np
from roboticstoolbox import DHRobot, RevoluteDH,RevoluteMDH
from spatialmath import SE3
import time
import roboticstoolbox as rtb
import math 
from scipy.spatial.transform import Rotation as R
import spatialmath.base as base
from sympy import *
import spatialmath.base.symbolic as sym

class HexaLeg(DHRobot):
    """
    Class that models a Hexa Cleaner leg

    :param symbolic: use symbolic constants
    :type symbolic: bool

    ``HexaLeg()`` is an object which models a hexa cleaner robot and
    describes its kinematic and dynamic characteristics using standard DH
    conventions.

    Defined joint configurations are:

    - qz, zero joint angle configuration
    - qr, arm horizontal along x-axis

    .. note::
        - SI units are used.

    """  # noqa

    def __init__(self, symbolic=False):
        
        if symbolic:
            zero = sym.zero()
            pi = sym.pi()
            half_pi = pi/2
            a0 = zero
            a1, a2, a3 = sym.symbol("a1 a2 a3")  # link
            theta1, theta2, theta3 = base.sym.symbol('ɵ1, ɵ2, ɵ3 ')
            theta4 = zero
            a = [a0,a1,a2,a3]
            d = [zero,zero,zero,zero]

            # dynamics paramters
            m1, m2, m3 = sym.symbol("m1 m2 m3")  # type: ignore
            m4 = zero 
            ms = [m1, m2, m3,m4]

            I1=[zero, zero, zero, zero, zero, zero]
            I2=[zero, zero, zero, zero, zero, zero]
            I3=[zero, zero, zero, zero, zero, zero]
            I4=[zero, zero, zero, zero, zero, zero]
            Is = [I1,I2,I3,I4]

            rl1, rl2,rl3 = sym.symbol("rl1 rl2 rl3")
            r1 = [rl1, zero, zero] # center of mass position with respect to ith link
            r2 = [rl2, zero, zero] # center of mass position with respect to ith link
            r3 = [rl3, zero, zero]
            r4 = [zero, zero, zero]
            rls = [r1,r2,r3,r4]

            thetas = [theta1, theta2, theta3,theta4]
            self.qz = np.array(thetas) 
            self.qr = np.array([theta1/2, theta2/2, theta3/2,theta4])
        else:
            pi = math.pi
            half_pi = pi/2.0
            zero = 0.0
            # robot length values (m)
            a = [0,0.045,0.075,0.140]
            d = [0,0,0,0]
            deg = pi / 180.0
            self.qr = np.array([10, 10, 10,10]) * deg
            self.qz = np.array([20, 20, 20,10]) * deg
            thetas = [10, 10, 10,10]

            m1, m2, m3 = 0.2,0.2,0.2  # type: ignore
            m4 = zero 
            ms = [m1, m2, m3,m4]

            I1=[zero, zero, zero, zero, zero, zero]
            I2=[zero, zero, zero, zero, zero, zero]
            I3=[zero, zero, zero, zero, zero, zero]
            I4=[zero, zero, zero, zero, zero, zero]
            Is = [I1,I2,I3,I4]

            rl1, rl2,rl3 = 0.045,0.075,0.14
            r1 = [rl1, zero, zero] # center of mass position with respect to ith link
            r2 = [rl2, zero, zero] # center of mass position with respect to ith link
            r3 = [rl3, zero, zero]
            r4 = [zero, zero, zero]
            rls = [r1,r2,r3,r4]

        alpha = [zero,half_pi, zero, zero]
        links = []

        for j in range(len(a)):
            link = RevoluteMDH(
                d=d[j], a=a[j], alpha=alpha[j],r=rls[j],m=ms[j],I=Is[j],Jm=zero,G=zero,B=zero,Tc=[zero,zero],qlim=[-pi,pi]
            )
            links.append(link)

        super().__init__(
            links,
            symbolic=symbolic,
            name="hexaleg",
            manufacturer="modi robotics",
        )

        self.addconfiguration("qr", self.qr)
        self.addconfiguration("qz", self.qz)

        # print transformation matrix
        for j in range(len(a)):
            
            print("Transformation matrix: "+str(j)+"_"+str(j+1)+str("_T:"))
            print(links[j].A(thetas[j]))

        #ets = self.ets()
        #print("ets is:"+str(ets))

def symbjacob():

    hexaleg = HexaLeg(symbolic=True)
    print("hexaleg symbolic: \n"+str(hexaleg))
    ## jacob end effector frame
    jacobe = hexaleg.jacobe(hexaleg.qz)
    sjacobe = simplify(jacobe)
    print("hexaleg.jacobe: \n"+str(sjacobe))

    ## jacob base effector frame
    jacob0 = hexaleg.jacob0(hexaleg.qz)
    sjacob0 = simplify(jacob0)
    print("hexaleg.jacob0: \n"+str(sjacob0))


def symbolic_dyna():

    theta1,theta2,theta3 = base.sym.symbol('ɵ1, ɵ2, ɵ3')
    thetad1,thetad2,thetad3 = base.sym.symbol('ɵ́1, ɵ́2, ɵ́3')
    thetadd1,thetadd2,thetadd3 = base.sym.symbol('ɵ̋1, ɵ̋2, ɵ̋2')
    zero = sym.zero()
    pi = sym.pi()
    grav_g = base.sym.symbol('g')

    thetas = [theta1,theta2,theta3,zero]
    thetads = [thetad1,thetad2,thetad3,zero]
    thetadds = [thetadd1,thetadd2,thetadd3,zero]
    gravs = [zero,grav_g,zero]


    robot = HexaLeg(symbolic=True)
    dynamat=robot.rne_python(Q=thetas,QD=thetads,QDD=thetadds,gravity=gravs)
    
    print("dynamat:\n")
    print(dynamat)
    simpdynamat = simplify(dynamat)

    print("simpdynamat:\n")
    for i in range(len(simpdynamat)):
        print("---\n")
        print(simpdynamat[i])

    robot.dynamics()

if __name__ == "__main__":  # pragma nocover
    #symbjacob()
    symbolic_dyna()

