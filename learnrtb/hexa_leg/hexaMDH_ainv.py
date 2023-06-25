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

        alpha = [zero,half_pi, zero, zero]
        self.links = []

        for j in range(len(a)):
            link = RevoluteMDH(
                d=d[j], a=a[j], alpha=alpha[j],qlim=[-pi,pi]
            )
            self.links.append(link)

        super().__init__(
            self.links,
            name="hexaleg",
            manufacturer="modi robotics",
        )

        self.addconfiguration("qr", self.qr)
        self.addconfiguration("qz", self.qz)

        # print transformation matrix
        for j in range(len(a)):
            
            print("Transformation matrix: "+str(j)+"_"+str(j+1)+str("_T:"))
            print(self.links[j].A(thetas[j]))

        #ets = self.ets()
        #print("ets is:"+str(ets))



    def ik3(self, T, config="lun"):

        config = self.config_validate(config, ("lr", "ud", "nf"))

        # solve for the first three joints

        a2 = self.links[1].a
        a3 = self.links[2].a
        d1 = self.links[0].d
        d3 = self.links[2].d
        d4 = self.links[3].d

        # The following parameters are extracted from the Homogeneous
        # Transformation as defined in equation 1, p. 34

        Px, Py, Pz = T.t
        Pz -= d1  # offset the pedestal height
        theta = np.zeros((3,))

        # Solve for theta[0]
        # r is defined in equation 38, p. 39.
        # theta[0] uses equations 40 and 41, p.39,
        # based on the configuration parameter n1

        r = np.sqrt(Px**2 + Py**2)
        if "r" in config:
            theta[0] = np.arctan2(Py, Px) + np.arcsin(d3 / r)
        elif "l" in config:
            theta[0] = np.arctan2(Py, Px) + np.pi - np.arcsin(d3 / r)
        else:
            raise ValueError("bad configuration string")

        # Solve for theta[1]
        # V114 is defined in equation 43, p.39.
        # r is defined in equation 47, p.39.
        # Psi is defined in equation 49, p.40.
        # theta[1] uses equations 50 and 51, p.40, based on the
        # configuration parameter n2
        if "u" in config:
            n2 = 1
        elif "d" in config:
            n2 = -1
        else:
            raise ValueError("bad configuration string")

        if "l" in config:
            n2 = -n2

        V114 = Px * np.cos(theta[0]) + Py * np.sin(theta[0])

        r = np.sqrt(V114**2 + Pz**2)

        with np.errstate(invalid="raise"):
            try:
                Psi = np.arccos(
                    (a2**2 - d4**2 - a3**2 + V114**2 + Pz**2)
                    / (2.0 * a2 * r)
                )
            except FloatingPointError:
                return "Out of reach"

        theta[1] = np.arctan2(Pz, V114) + n2 * Psi

        # Solve for theta[2]
        # theta[2] uses equation 57, p. 40.
        num = np.cos(theta[1]) * V114 + np.sin(theta[1]) * Pz - a2
        den = np.cos(theta[1]) * Pz - np.sin(theta[1]) * V114
        theta[2] = np.arctan2(a3, d4) - np.arctan2(num, den)

        theta = base.angdiff(theta)

        print("theta: "+str(theta) )
        return theta

    


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


def numericjacob():
    hexaleg = HexaLeg(symbolic=False)
    print("hexaleg numeric: \n"+str(hexaleg))
    #hexaleg.plot(hexaleg.qr)
    #time.sleep(10)
if __name__ == "__main__":  # pragma nocover
    symbjacob()
    numericjacob()
    

