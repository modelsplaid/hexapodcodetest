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
from math import pi
from pprint import pprint
import matplotlib as mpl
import matplotlib.pyplot as plt
from copy import deepcopy
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

    def __init__(self, symbolic=False,coxia_m=0.045,\
        femur_m=0.075,tibia_m=0.140,m1_kg=0,m2_kg=0,m3_kg=0,m4_kg=0):
        
        if symbolic: # for symbolic computation
            
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
        
        else: # for numeric computation
            pi = math.pi
            half_pi = pi/2.0
            zero = 0.0
            
            # robot length values (m)
            a = [0,coxia_m,femur_m,tibia_m]
            d = [0,0,0,0]
            deg = pi / 180.0
            self.qr = np.array([0,0,0,0]) * deg
            self.qz = np.array([0,0,0,0]) * deg
            thetas = [0, 0, 0,0]
            
            # link mass
            ms = [m1_kg, m2_kg, m3_kg,m4_kg]

            # link inertial 
            I1=[zero, zero, zero, zero, zero, zero]
            I2=[zero, zero, zero, zero, zero, zero]
            I3=[zero, zero, zero, zero, zero, zero]
            I4=[zero, zero, zero, zero, zero, zero]
            Is = [I1,I2,I3,I4]

            # link mass center 
            rl1, rl2,rl3 = 0.045,0.075,0.15
            r1 = [rl1, zero, zero] # center of mass position with respect to ith link
            r2 = [rl2, zero, zero] # center of mass position with respect to ith link
            r3 = [rl3, zero, zero]
            r4 = [zero, zero, zero]
            rls = [r1,r2,r3,r4]

        alpha = [zero,half_pi, zero, zero]
        links = []

        for j in range(len(a)):
            link = RevoluteMDH(
                d=d[j], a=a[j], alpha=alpha[j],
                r=rls[j],m=ms[j],I=Is[j],
                Jm=zero,G=zero,Tc=[zero,zero],
                qlim=[-pi,pi]
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

        ## print transformation matrix
        #for j in range(len(a)):
        #    
        #    print("Transformation matrix: "+str(j)+"_"+str(j+1)+str("_T:"))
        #    print(links[j].A(thetas[j]))



    def plot_sqs(self,data=[[0,0,0]],ylabel = ""):
        
        ptdata = deepcopy(data)
        plt.subplot(211)
        plt.plot(ptdata,'*')
        plt.ylabel(ylabel)
        plt.show(block=True)
        

    def inv_leg_sqs(self,start_pose_rad = [0,0,-pi/2,0],target_pose_sqs_m = [[0,0,0]]):
        q_target_sqs = np.array([[0,0,0,0]],np.float64)

        # First 
        q_target = self.inv_leg(start_pose_rad,target_pose_sqs_m[0])
        q_target_sqs[0] = q_target
        
        # Remaining
        for i in range(1,len(target_pose_sqs_m)):
            q_target = self.inv_leg(start_pose_rad,target_pose_sqs_m[i])
            #print("q_target_sqs:\n"+str(q_target_sqs)) 
            #print("q_target:\n"+str(q_target)) 
            q_target_sqs = np.concatenate((q_target_sqs,[q_target]))
        return q_target_sqs

    def inv_leg(self,start_pose_rad = [0,0,-pi/2,0],target_pose_m = [0,0,0]):
        #start_pose_m = [0.12,0,-0.14]
        #target_pose_m = [0.12,0.03,-0.14]
        T = SE3(target_pose_m)

        mat_start = self.fkine(start_pose_rad)
        #print("mat_start: \n"+str( mat_start))
        #print("type: \n"+str( type(mat_start)))

        q_target = self.ikine_LMS(T,mask=[1,1,1,0,0,0],q0=start_pose_rad)
        #q_target = self.ik_lm_chan(T,mask=[1,1,1,0,0,0],q0=start_pose_rad)
        #print("q_target[0]: \n"+str(q_target[0]))
        mat_target = self.fkine(q_target[0] )
        #print("mat_target: \n"+str(mat_target))
        
        return q_target[0]

    def ctraj_gen_sqs(self,start_pose_m,start_pose_rad,end_point_m,num_inter_pts):

        # Descritize a line in to num_inter_pts number of points 
        traj_m_sqs = rtb.jtraj(start_pose_m, end_point_m, num_inter_pts)
        #print("traj_m_sqs.t:\n" + str(traj_m_sqs.t))
        print("traj_m_sqs.s:\n" + str(traj_m_sqs.s))
        traj_m_sqs = traj_m_sqs.s
        # The corresponding joint angle on the path of given moving points
        ctraj_rad_sqs = self.inv_leg_sqs(start_pose_rad,traj_m_sqs)
        
        print("Joint moving range: \n"+ str(ctraj_rad_sqs[-1]-ctraj_rad_sqs[0]))
        return ctraj_rad_sqs

    def trans_jacob0(self,jtraj_sqs_rad = [[0,0,0,0]]):
        
        # This is to calculate joint torque by providing cartesian force 
        # on end effector and joint pose

        trans_jacob_sqs = []

        for trjaj_rad in jtraj_sqs_rad:
            #print("trjaj_rad:\n "+str(jtraj_sqs_rad) )
            jacob0_mat = self.jacob0(trjaj_rad)

            v_jacob = np.array([[0,0,0],[0,0,0],[0,0,0]],np.float64)

            # Extract velocity part of jacobian
            for i in range(3):
                v_jacob[i] = jacob0_mat[i][0:3]
            
            # Compute transpose
            trans_v_jacob = np.transpose(v_jacob)

            trans_jacob_sqs.append(trans_v_jacob)
        
        return trans_jacob_sqs

    def inv_trans_jacob0(self,jtraj_sqs_rad = [[0,0,0,0]]):
        #This is to calculate  cartesian force on end effector by providing 
        # joint forces and joint pose

        trans_inv_jacob_sqs = []

        for trjaj_rad in jtraj_sqs_rad:
            #print("trjaj_rad:\n "+str(jtraj_sqs_rad) )
            jacob0_mat = self.jacob0(trjaj_rad)

            v_jacob = np.array([[0,0,0],[0,0,0],[0,0,0]],np.float64)

            # Extract velocity part of jacobian
            for i in range(3):
                v_jacob[i] = jacob0_mat[i][0:3]
            
            # Compute transpose
            trans_v_jacob = np.transpose(v_jacob)
            
            # 
            # Compute inverse
            inv_v_jacob = np.linalg.inv(trans_v_jacob)
            #print("inv_v_jacob: \n"+str(inv_v_jacob) )

            trans_inv_jacob_sqs.append(inv_v_jacob)
        
        return trans_inv_jacob_sqs


    def inv_jacob0(self,jtraj_sqs_rad = [[0,0,0,0]]):
        inv_jacob_mat_sqs = []

        for trjaj_rad in jtraj_sqs_rad:
            #print("trjaj_rad:\n "+str(jtraj_sqs_rad) )
            jacob0_mat = self.jacob0(trjaj_rad)

            v_jacob = np.array([[0,0,0],[0,0,0],[0,0,0]],np.float64)

            # Extract velocity part of jacobian
            for i in range(3):
                v_jacob[i] = jacob0_mat[i][0:3]
            
            inv_v_jacob = np.linalg.inv(v_jacob)
            #print("inv_v_jacob: \n"+str(inv_v_jacob) )

            inv_jacob_mat_sqs.append(inv_v_jacob)
        
        return inv_jacob_mat_sqs

    def dot_mat_sqs_vec(self,mat_sqs,vec):
        # Given sequence of matrix, and a vecotor. 
        # Do dot product and return result vecotor sequence
        result_vec_sqs = []
        for mat in mat_sqs: 
            jtorq_nm = np.dot(mat , vec)
            result_vec_sqs.append(jtorq_nm)
        
        #print("jtorq_sqs_nm: \n"+str(jtorq_sqs_nm))        
        return result_vec_sqs

    def cal_cartf_by_jtorq(self,inv_tran_jacob_mat_sqs,torq_nm):
        # Gvien force vector in catesian vector for end effector 
        # calculate torq for each motor
        eforce_sqs_nm = self.dot_mat_sqs_vec(inv_tran_jacob_mat_sqs,torq_nm)     
        
        return eforce_sqs_nm

    def cal_jtorq_by_cartf(self,tran_jacob_mat_sqs,cart_force_n):
        # Gvien force vector in catesian vector for end effector 
        # calculate torq for each motor
        jtorq_sqs_nm = self.dot_mat_sqs_vec(tran_jacob_mat_sqs,cart_force_n)     
        
        return jtorq_sqs_nm

    def cal_jspd_rads(self,inv_jacob_mat_sqs,cart_mov_spd_msec):

        jspd_sqs_rads = self.dot_mat_sqs_vec(inv_jacob_mat_sqs,cart_mov_spd_msec)         
        return jspd_sqs_rads

    def cal_jtime_sqs(self,jspd_sqs_rads,jtraj_rad):
        jtim_sqs_msec = []
        for i in range(1,len(jtraj_rad)):
            jtraj_diffs = jtraj_rad[i]-jtraj_rad[i-1]
            jtraj_spds = (jspd_sqs_rads[i]+jspd_sqs_rads[i-1])/2.0

            #jtraj_diffs = jtraj_rad[i]
            #jtraj_spds = jspd_sqs_rads[i]
            
            #print("jtraj_spds: \n"+str(jtraj_spds)) 
            #print("jtraj_diffs: \n"+str(jtraj_diffs)) 

            jtim_sec = [0,0,0,0]
            for idx in range(len(jtraj_spds)): # t = d/v
                if np.abs(jtraj_spds[idx] == 0):
                    #print("!!!!!!!!!!! Getting zero value !!!!!!!!!!!!")
                    jtim_sec[idx] = 0.0
                elif np.abs(jtraj_spds[idx])<0.0001:
                    jtim_sec[idx] = 0.0
                    #print("!!!Getting exteme value: jtraj_spds[idx]: "+str(jtraj_spds[idx])+\
                    #    " trajectory number: "+str(i) + "joint number: " + str(idx)
                    #    )
                    #print("traj num: "+str(i)+" joint num: "+str(idx)  )
                    #jtim_sec[idx] = jtraj_diffs[idx]/jtraj_spds[idx]
                else:
                    jtim_sec[idx] = abs(jtraj_diffs[idx]/jtraj_spds[idx])
      
                
            jtim_msec = np.dot(jtim_sec,1000) # convert to milisecond

            for i in range(len(jtim_msec)): # convert to int
                jtim_msec[i] = int(jtim_msec[i])

            jtim_sqs_msec.append(jtim_msec)
            
            #print("jtim_msec:  "+str(jtim_msec) )

        #print("jtim_sqs_msec:\n "+str(jtim_sqs_msec) )
        
        total_run_time = [0,0,0,0]
        for jtim in jtim_sqs_msec:
            total_run_time = np.add(total_run_time,np.abs(jtim))
        print("total_run_time: \n"+str(total_run_time) )

        return jtim_sqs_msec

    def symbjacob(self):    
        ## jacob end effector frame
        jacobe = self.jacobe(self.qz)
        sjacobe = simplify(jacobe)
        print("self.jacobe: \n"+str(sjacobe))

        ## jacob base effector frame
        jacob0 = self.jacob0(self.qz)
        sjacob0 = simplify(jacob0)
        print("self.jacob0: \n"+str(sjacob0))


    def numericjacob(self):
        pass
        #hexaleg = HexaLeg(symbolic=False)
        #print("hexaleg numeric: \n"+str(hexaleg))
        #hexaleg.plot(hexaleg.qr)
        #time.sleep(10)



if __name__ == "__main__":  # pragma nocover
    #    symbjacob()
    #    numericjacob()
    hleg = HexaLeg()
    hleg.inv_leg()
    

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

  
if __name__ == "__main__":
    #symbjacob()
    symbolic_dyna()