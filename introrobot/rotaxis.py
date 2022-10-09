from math import *
import numpy as np

def rotaxis(kx,ky,kz,theta):
    r11 =kx*kx* (1-cos(theta)) + cos(theta)
    r21 =kx*ky* (1-cos(theta)) + kz*sin(theta)
    r31 =kx*kz* (1-cos(theta)) - ky*sin(theta)

    r12 =kx*ky* (1-cos(theta)) - kz*sin(theta)
    r22 =ky*ky* (1-cos(theta)) + cos(theta)
    r32 =ky*kz* (1-cos(theta)) + kx*sin(theta)

    r13 =kx*kz* (1-cos(theta)) + ky*sin(theta)
    r23 =ky*kz* (1-cos(theta)) - kx*sin(theta)
    r33 =kz*kz* (1-cos(theta)) + cos(theta)


    r11 = round(r11,3)
    r21 = round(r21,3)
    r31 = round(r31,3)
    r12 = round(r12,3)
    r22 = round(r22,3)
    r32 = round(r32,3)
    r13 = round(r13,3)
    r23 = round(r23,3)
    r33 = round(r33,3)
    rotmat = np.array([[r11,r21,r31],[r12,r22,r32],[r13,r23,r33]])
    print("rotmat: \n"+str(rotmat) )
    

rotaxis(0.58,0.58,0.58,pi/4)