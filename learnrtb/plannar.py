"""
@author: Luis Fernando Lara Tobar
@author: Peter Corke
@author: Samuel Drew
"""

from roboticstoolbox import DHRobot, RevoluteDH
import numpy as np
from math import pi


class Planar3(DHRobot):
    """
    Class that models a planar 3-link robot

    ``Planar2()`` is a class which models a 3-link planar robot and
    describes its kinematic characteristics using standard DH
    conventions.

    .. runblock:: pycon

        >>> import roboticstoolbox as rtb
        >>> robot = rtb.models.DH.Planar3()
        >>> print(robot)

    Defined joint configurations are:

        - qz, zero angles, all folded up

    .. note::

      - Robot has only 3 DoF.

    .. codeauthor:: Peter Corke
    """

    def __init__(self):

        L = [RevoluteDH(a=1), RevoluteDH(a=1), RevoluteDH(a=1)]

        super().__init__(L, name="Planar 3 link", keywords=("planar",))

        self.qr = [1.5,1.5,1.5]
        self.qz = [0.75,0.75,0.75]

        self.addconfiguration("qr", self.qr)
        self.addconfiguration("qz", self.qz)


if __name__ == "__main__":  # pragma nocover

    robot = Planar3()
    
    print(robot)
    deg = pi / 180
    qr = np.array([10.1, 19.3, 29.6]) * deg

    # target location  
    qt = np.array([10.7, 20.7, 30.7]) * deg

    mat_target = robot.fkine(qt)
    print("mat_target: \n"+str(mat_target))

    q_target = robot.ik_gn(mat_target,q0=qr, we=[1,1,1,0,0,0],slimit=10)

    print("robot.ets(): \n"+str(robot.ets()) )
    print("q_target:"+str(q_target) )
    print("q_target:" )
    print(q_target[0]/deg)

