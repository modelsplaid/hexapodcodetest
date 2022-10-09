import numpy as np
from roboticstoolbox import DHRobot, RevoluteDH,RevoluteMDH
from spatialmath import SE3
import time
import roboticstoolbox as rtb
from math import pi
from scipy.spatial.transform import Rotation as R
import spatialmath.base as base
from sympy import *

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
            import spatialmath.base.symbolic as sym

            zero = sym.zero()
            pi = sym.pi()
            half_pi = pi/2
            a1, a2, a3 = sym.symbol("a1 a2 a3")  # link
            theta1, theta2, theta3 = base.sym.symbol('ϴ1, ϴ2, ϴ3 ')
            a = [a1,a2,a3]
            d = [zero,zero,zero]

            self.qz = np.array([theta1, theta2, theta3]) 
            self.qr = np.array([theta1/2, theta2/2, theta3/2])
        else:
            from math import pi
            half_pi = pi/2
            zero = 0.0
            # robot length values (m)
            a = [0.045,0.075,0.140]
            d = [0,0,0]
            deg = pi / 180.0
            self.qr = np.array([10, 10, 10]) * deg
            self.qz = np.array([20, 20, 20]) * deg

        alpha = [half_pi, zero, zero]
        links = []

        for j in range(len(a)):
            link = RevoluteDH(
                d=d[j], a=a[j], alpha=alpha[j],qlim=[0,pi]
            )
            links.append(link)

        super().__init__(
            links,
            name="hexaleg",
            manufacturer="modi robotics",
        )


        self.addconfiguration("qr", self.qr)
        self.addconfiguration("qz", self.qz)

        #ets = self.ets()
        #print("ets is:"+str(ets))

def symbjacob():


    hexaleg = HexaLeg(symbolic=True)
    ## jacob end effector frame
    jacobe = hexaleg.jacobe(hexaleg.qz)
    sjacobe = simplify(jacobe)
    print("hexaleg.jacobe: \n"+str(sjacobe))

    ## jacob base effector frame
    jacob0 = hexaleg.jacob0(hexaleg.qz)
    sjacob0 = simplify(jacob0)
    print("hexaleg.jacob0: \n"+str(sjacob0))


def numericjacob():
    hexaleg = HexaLeg(symbolic=False)
    print("hexaleg: \n"+str(hexaleg) )

if __name__ == "__main__":  # pragma nocover
    symbjacob()
    numericjacob()

