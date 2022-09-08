import numpy as np
from roboticstoolbox import DHRobot, RevoluteDH,RevoluteMDH
from spatialmath import SE3
import time
import roboticstoolbox as rtb
from math import pi
from scipy.spatial.transform import Rotation as R

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
        else:
            from math import pi

            zero = 0.0

        deg = pi / 180

        # robot length values (mm)
        a = [0.045,0.075,0.140]
        d = [0,0,0]

        alpha = [pi / 2, zero, zero]

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

        self.qr = np.array([10, 10, 10]) * deg
        self.qz = np.array([20, 20, 20]) * deg

        self.addconfiguration("qr", self.qr)
        self.addconfiguration("qz", self.qz)

        ets = self.ets()
        print("ets is:"+str(ets))

def testparams():
    deg = pi / 180

    hexaleg = HexaLeg(symbolic=False)
    print(hexaleg)

    qz = np.array([0, 0, 0]) * deg
    qr = np.array([90, 0, 0]) * deg
    ets = hexaleg.ets()
    print("ets:"+str(ets))

    Te = hexaleg.fkine([0,0,0])
    print("Te: \n"+str(Te))

    #traj = hexaleg.jtraj(qz,qr,10)
    #rtb.qplot(traj.q)

    #while True:
    #    hexaleg.plot(hexaleg.qr)
    #    time.sleep(0.1)
    # print(ur3.dyntable())



def testinv():
    deg = pi / 180

    hexaleg = HexaLeg(symbolic=False)
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


def testEulerAngle():
    r = R.from_matrix([[0.6131, 0.7678, 0.1857],
                        [0.1158, 0.1451, -0.9826],
                        [-0.7814, 0.624, 0]])
    print("rotvec: "+ str(r.as_rotvec()))

    print("euler:" +  str(r.as_euler('xyz', degrees=True)))


def testjtraj():
    deg = pi / 180
    qs = np.array([10.1, -19.3, -29.6]) * deg
    qt = np.array([15.1, 10.3, -20.6]) * deg

    traj = rtb.jtraj(qs, qt, 10)
    #print("robotraj arrive: \n"+str(traj.arrive ))
    print("robotraj info: \n"+str(traj.t))
    print("robotraj via: \n"+str(traj.s ))

    hexaleg = HexaLeg(symbolic=False)
    #print(hexaleg)
    #hexaleg.plot(traj.s,eeframe=True,jointaxes=True)

if __name__ == "__main__":  # pragma nocover
    #testinv()
    #testEulerAngle()
    testjtraj()
    testparams()
