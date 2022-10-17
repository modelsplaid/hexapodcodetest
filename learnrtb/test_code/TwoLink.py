"""
@author: Peter Corke
"""

from roboticstoolbox import DHRobot, RevoluteDH
# from math import pi
from spatialmath import SE3
import numpy as np
import numpy as np
import spatialmath.base as base
import time
#from math import *
from sympy import *
import spatialmath.base.symbolic as sym

class TwoLink(DHRobot):
    """
    Class that models a 2-link robot moving in the vertical plane

    :param symbolic: use symbolic constants
    :type symbolic: bool

    ``TwoLink()`` is a class which models a 2-link planar robot and
    describes its kinematic and dynamic characteristics using standard DH
    conventions. of a simple planar 2-link mechanism moving in the xz-plane, it experiences gravity loading.
    All mass is concentrated at the joints.

    .. runblock:: pycon

        >>> import roboticstoolbox as rtb
        >>> robot = rtb.models.DH.TwoLink()
        >>> print(robot)

    The parameters values depend on the ``symbolic`` parameter

    =======================================  =================  ==============
    Parameters                               Numeric values     Symbolic values
    =======================================  =================  ==============
    link lengths                             1, 1               a1, a2
    link masses                              1, 1               m1, m2
    link CoMs in the link frame x-direction  -0.5, -0.5         c1, c2
    gravitational acceleration               9.8                g
    =======================================  =================  ==============

    Defined joint configurations are:

        - qz, zero angles, all folded up
        - q1, links are horizontal and vertical respectively
        - q2, links are vertical and horizontal respectively
        - qn, nominal working configuration

    .. note::

        - Robot has only 2 DoF.
        - Motor inertia is 0.
        - Link inertias are 0.
        - Viscous and Coulomb friction is 0.

    :Reference: Based on Fig 3-6 (p73) of Spong and Vidyasagar (1st edition).

    .. codeauthor:: Peter Corke
    """

    def __init__(self, symbolic=False):

        if symbolic:
            import spatialmath.base.symbolic as sym

            zero = sym.zero()
            pi = sym.pi()
            a1, a2 = sym.symbol("l1 l2")  # type: ignore
            m1, m2 = sym.symbol("m1 m2")  # type: ignore
            #c1, c2 = sym.symbol("c1 c2")  # type: ignore
            c1= a1 #sym.symbol("c1 c2")  # type: ignore
            c2= a2
            g = sym.symbol("g")
        else:
            from math import pi

            zero = 0.0
            a1 = 1
            a2 = 1
            m1 = 1
            m2 = 1
            c1 = -0.5
            c2 = -0.5
            g = 9.8

        links = [
            RevoluteDH(a=a1, alpha=zero, m=m1, r=[c1, 0, 0]),
            RevoluteDH(a=a2, alpha=zero, m=m2, r=[c2, 0, 0]),
        ]

        super().__init__(
            links, symbolic=symbolic, name="2 link", keywords=("planar", "dynamics")
        )

        self.qr = np.array([pi / 6, -pi / 6])
        self.qz = np.zeros(2)

        self.addconfiguration("qr", self.qr)
        self.addconfiguration("qz", self.qz)

        self.addconfiguration_attr("qz", [0, 0])
        self.addconfiguration_attr("q1", [0, pi / 2])
        self.addconfiguration_attr("q2", [pi / 2, -pi / 2])
        self.addconfiguration_attr("qn", [pi / 6, -pi / 6])

        self.base = SE3.Rx(pi / 2)
        self.gravity = [0, g, 0]

def symbolic_dyna():

    theta1,theta2 = base.sym.symbol('ɵ1, ɵ2')
    thetad1,thetad2 = base.sym.symbol('ɵ́1, ɵ́2')
    thetadd1,thetadd2 = base.sym.symbol('ɵ̋1, ɵ̋2')
    zero = sym.zero()
    pi = sym.pi()
    grav_g = base.sym.symbol('g')

    thetas = [theta1,theta2]
    thetads = [thetad1,thetad2]
    thetadds = [thetadd1,thetadd2]
    gravs = [zero,grav_g,zero]


    robot = TwoLink(symbolic=True)
    dynamat=robot.rne_python(Q=thetas,QD=thetads,QDD=thetadds,gravity=gravs)
    
    print("dynamat:\n")
    print(dynamat)
    simpdynamat = simplify(dynamat)

    print("simpdynamat:\n")
    for i in range(len(simpdynamat)):
        print("---\n")
        print(simpdynamat[i])

if __name__ == "__main__":  # pragma nocover
    symbolic_dyna()
    #robot = TwoLink(symbolic=True)
    #print(robot)
