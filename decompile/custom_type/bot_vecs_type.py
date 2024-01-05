import sys
import numpy as np 
import math 
sys.path.append("../")

from    copy                     import deepcopy
from    typing                   import List
from    spatialmath              import SE3
from    custom_type.hexagon_type import HexgnTranType

print("bot_vecs_type.py")

class BotVec:
    
    def __init__(self,name='',*args,**kwds):

        """
        Case 1 Init without param: 
                a = BotVec()

        Case 2: Init with given param names:
                a = BotVec("bv",x=1,y=2,z=3,i=99) (i stands for id)

        Case 3: Init with list point and param names:
                a = BotVec("bv",[-1,-2,-3],i=98) (i stands for id)
        
        Case 4: Init with list point and ik value:
                a = BotVec("c",[4,5,6],97)
        
        Case 5: Init with only name and list point:
                a = BotVec("d",[7,8,9])

        Case 6: Init with Only list point: 
                a = BotVec([7,8,9])

        Case 7: Init with all separate number
                mid = BotVec("mid_leg",1,20,3,7)

        Case 8: Init with 3 coordinate value
                rft = BotVec("rft_leg",4,5,6)
        """

        self.x      = 0
        self.y      = 0
        self.z      = 0
        self.name   = ""
        self.leg_id = 0
        
        # Case 2,3
        if len(kwds.keys())!=0:
            self.name = name
            for k in kwds.keys():
                if k == "x": 
                    self.x = kwds[k]
                elif k == "y": 
                    self.y = kwds[k]
                elif k == "z":
                    self.z = kwds[k]
                elif k == "i":
                    self.leg_id = kwds[k]
        # Case 4,5
        if len(args) !=0:
            self.name = name
            if len(args)==1 and isinstance(args[0],List) and len(args[0])==3 :
                self.x = args[0][0]
                self.y = args[0][1]
                self.z = args[0][2]
            
            if len(args)==2 and isinstance(args[0],List) and len(args[0])==3 \
                            and isinstance(args[1],int):
                self.x = args[0][0]
                self.y = args[0][1]
                self.z = args[0][2]
                self.leg_id = args[1]

            if len(args)==3 :
                self.x = args[0]
                self.y = args[1]
                self.z = args[2]

            if len(args)==4 :
                self.x = args[0]
                self.y = args[1]
                self.z = args[2]
                self.leg_id = args[3]
            


        # Case 6
        if isinstance(name,List) and len(name)==3:
            self.name = ""
            self.x = name[0]
            self.y = name[1]
            self.z = name[2]

  

    def subtract(self,right_vec:'BotVec'):
        """
        Current vec subtract given vec. 
        """
        result = self.clone()

        a = self.x - right_vec.x
        b = self.y - right_vec.y
        c = self.z - right_vec.z

        result.set_pt_arr([a,b,c])

        return result

    @staticmethod
    def skew(p:"BotVec"):
        return np.array([[0, -p.z, p.y], [p.z, 0, -p.x], [-p.y, p.x, 0]])

    def align_given_vec(self,ref_vec:'BotVec'=None)->SE3:
        '''
        Given a vector, calculate the rotation which align self vector. 
        Type ref_vec: BotVec
        Return: SE3 matrix, contains roo and pitch rotation  
        
        https://math.stackexchange.com/questions/180418/calculate-rotation-matrix-to-align-vector-a-to-vector-b-in-3d
        '''
        if(ref_vec==None):
            ref_vec = BotVec("z-vec",[0,0,1])

        v = self.cross_prdct(ref_vec)
        s = v.l2_norm()

        # When angle between a and b is zero or 180 degrees
        # cross product is 0, R = I
        if s == 0.0:
            rse3 = SE3(np.eye(4),check=False)
            return rse3
    
        c = self.dot_prdct(ref_vec)
        i = np.eye(3)  # Identity matrix 3x3

        # skew symmetric cross product
        vx = self.skew(v)
        d = (1 - c) / (s * s)
        r = i + vx + np.matmul(vx, vx) * d

        # tood: -> se3 

        # r00 r01 r02 0
        # r10 r11 r12 0
        # r20 r21 r22 0
        #  0   0   0  1
        r = np.hstack((r, [[0], [0], [0]]))
        r = np.vstack((r, [0, 0, 0, 1]))
         
        #rse3=SE3(np.array(r),check=False) # note: try this if raise error for below code
        rse3 = SE3(np.array(r))

        return rse3
    
    def clone(self):
        """
        Clone a copy of self-object 
        """
        cls    = self.__class__
        result = cls.__new__(cls)

        # copy value 
        result.x    = self.x  
        result.y    = self.y
        result.z    = self.z
        result.name = self.name
        result.leg_id   = self.leg_id

        return result
    
    def cross_prdct(self,p_vec:"BotVec"):
        """
        Cross product of two vectors. self-cross-p_vec
        Param : type p_vec: BotVec
        Return : type BotVec
        """
        vec_a = self.get_pt_arr()
        vec_b = p_vec.get_pt_arr()

        res = self.clone()
        if isinstance(p_vec,BotVec):
            cab = np.cross(vec_a,vec_b)
            res.set_pt_arr(list(cab))
            return res
        else:
            return None
        
    def l2_norm(self)->float:
        """
        Return vector length (l2 norm)
        Return type: float
        """
        sqn = self.x**2+self.y**2+self.z**2
        l2norm = math.sqrt(sqn)
        return l2norm
     
    def dot_prdct(self,p):
        """
        Dot product of two vectors. self-dot-p_vec
        Param : type p: BotVec
                type p: float

        return: type float 
        """
        vec_a = self.get_pt_arr()
        if isinstance(p,BotVec):
            vec_p = p.get_pt_arr()
            dab = np.dot(vec_a,vec_p)
            return dab
        elif isinstance(p,float) or isinstance(p,int):
            res = self.clone()

            dab = np.dot(vec_a,p)
            res.set_pt_arr(list(dab))

            return res
        else:
            return None

    def mat_dot_self(self,trans:SE3):
        """
        Given translation matrix , update new point 
        Param : tran_cob: Given tans matrix
        return: Transformed BotCartType object
        """

        result = self.clone()

        # Translate matrices
        tran_arr = trans*self.get_pt_arr()

        [nam,id] = self.get_leg_name_id()
        name = "trans from " +nam+": "
        
        result.set_pt_arr([tran_arr[0][0],
                           tran_arr[1][0],
                           tran_arr[2][0]],name,id)
        
        return result

    def form_str(self):
        full_str = ""
        full_str = full_str + str(self.name) +": "
        full_str = full_str + "x: "+ f"{self.x     :+5.2f}, "
        full_str = full_str + "y: "+ f"{self.y     :+5.2f}, "
        full_str = full_str + "z: "+ f"{self.z     :+5.2f}, "
        full_str = full_str + "i: "+ f"{self.leg_id:+5.2f}, "

        return full_str   

    def get_pt_arr(self)->List:
        """
        Return [x,y,z]
        """
        return [self.x,self.y,self.z]
    
    def get_leg_name_id(self)->List:
        """
        return: [self.name,self.leg_id ]
        type  : [str      , nt      ]
        """
        return [self.name,self.leg_id]
    
    def get_leg_id(self)->int:
        """
        return: [self.name,self.leg_id ]
        type  : int
        """
        return self.leg_id

    def set_pt_arr(self,pt_arr=[0,0,0],name:str='',leg_id:int=0)->List:
        """
        Param pt_arr: [x,y,z]
        """
        self.x = pt_arr[0]
        self.y = pt_arr[1]
        self.z = pt_arr[2]
        self.name   = name 
        self.leg_id = leg_id

        
    def __sub__(self,right_vec:'BotVec'):
        if isinstance(right_vec,BotVec):
            return self.subtract(right_vec)
        else :
            return NotImplemented   

    def __mul__(self,p):
        """
        Dot product of two vectors. self-dot-p_vec
        Param : type p: BotVec
                type p: float
        Exampe:     a = BotVec("a",[1,0,0])
                    b = BotVec("b",[0,1,0])
                    s = 3.0

                    c = a*b 
                    d = a*s 

        return: type float 
        """

        if isinstance(p,BotVec) or isinstance(p,float) or isinstance(p,int):
            result = self.dot_prdct(p)

            return result
        else:
            return NotImplemented    
        
    def __rmul__(self,tran:SE3):
        """
        Given translation matrix, update transformed point 
            e.g: 

        Param : tran: Given tans matrix
        return: Transformed BotVec object
        """

        if isinstance(tran,SE3): 
            result = self.mat_dot_self(tran)

            return result
        else:
            return NotImplemented    

    def __str__(self):
        full_str = self.form_str()
        return full_str


class BotVecArr:

    def __init__(self,name='',vec_len=0):
        """
        Param: vec_len: Create vector array with given length
        """
        self.vec_list = [BotVec()]*vec_len
        self.name = name

    def form_str(self):
        fullstr = ""
        fullstr = fullstr+self.name +"\n"

        for i in range(len(self.vec_list)):
            fullstr = fullstr + self.vec_list[i].form_str()+"\n"
        
        return fullstr
    
    def get_pt_by_id(self,id:int)->BotVec:
        i=0
        for pt in self.vec_list:

            if id == pt.get_leg_id():
                return self[i]
            i+=1
            

    def if_id_in_it(self,id:int=0)->bool:
        ids = []
        for pt in self.vec_list:
            ids = ids + [pt.get_leg_id()]
        
        if id in ids: 
            return True 
        else: 
            return False 

    def cmput_lowst_pt(self,axis:str='z')->BotVec:

        """
        Given an axis, return the lowest point on this axis
        Param axis: 'x', 'y','z' 
        Return    : A point in type of BotVec 

        """
        def argmin(iterable):
            return min(enumerate(iterable), key=lambda x: x[1])[0]
            
        if axis == 'z':
            z = []
            for i in range(self.get_len()):
                z = z + [self.get_ivec(i).z]
            imin = argmin(z)
            minv = self.get_ivec(imin)
            minv.name = minv.name + " has min-z"
            return minv

        if axis == 'y':
            y = []
            for i in range(self.get_len()):
                y = y + [self.get_ivec(i).y]
            imin = argmin(y)
            minv = self.get_ivec(imin)
            minv.name = minv.name + " has min-y"
            return minv
        
        if axis == 'x':
            x = []
            for i in range(self.get_len()):
                x = x + [self.get_ivec(i).x]
            imin = argmin(x)
            minv = self.get_ivec(imin)
            minv.name = minv.name + " has min-x"
            return minv

    def clone(self):
        """
        Clone a copy of self-object 
        """
        cls    = self.__class__
        result = cls.__new__(cls)

        # copy value 
        result.name = self.name
        result.vec_list = self.vec_list
        return result
    
    def mat_dot_self(self,trans:SE3):
        """
        Given translation matrix , update new point 
        Param : tran_cob: Given tans matrix
        return: Transformed BotCartType object
        """
        result = self.clone()
        # Translate matrices
        for i in range(len(self.vec_list)):
            pt = self.get_ivec(i)
            result.set_ivec(i,trans*pt)

        # copy value 
        result.name = "trans from " +self.name+": "
        return result
    
    def mats_dot_self(self,trans:HexgnTranType):
        result = self.clone()
        for i in range(len(self.vec_list)):
            pt = self.get_ivec(i)
            [nam,id] = pt.get_leg_name_id()
            tran = trans[id]
            result.set_ivec(i,tran*pt)
        result.name = "trans from " +self.name+": "
        return result

        
    def get_len(self):
        return len(self.vec_list)
    
    def get_name(self):
        return self.name 
    
    def get_ivec(self,i:int=0)->BotVec:
        return deepcopy(self.vec_list[i])
    
    def get_by_axis(self,axis_nam:str='x')->List:

        """
        Get all values for axis x or y or z 
        Param axis_nam: choices: 'x', 'y' , 'z'
        """
        
        axis_lst = [0]*self.get_len()
        for i in range(self.get_len()):
            if axis_nam == 'x':
                axis_lst[i] = self[i].x
            if axis_nam == 'y':
                axis_lst[i] = self[i].y
            if axis_nam == 'z':
                axis_lst[i] = self[i].z

        return axis_lst
    
    def set_name(self,name=""):
        self.name = name 

    def set_ivec(self,i:int=0,vec:BotVec=None):
        if BotVec == None: 
            return None
        self.vec_list[i] = deepcopy(vec)

    def __str__(self):
        full_str = self.form_str()
        return full_str
    
    def __len__(self):
        return self.get_len()

    def __rmul__(self,tran):
        """
        Given translation matrix, update transformed point 

        Case 1 SE3 type: 
                ba = BotVecArr("ba",5)
                t = SE3.Trans(3.14,2,1)
                ca = t*ba

 
        Case 2 HexgnTranType:
            mid = BotVec("mid_leg",1,2,3,0)
            rft = BotVec("rft_leg",1,2,3,1)
            pts_wbase = BotVecArr("ptb",0)
            pts_wbase +=mid
            pts_wbase +=rft
            cob2base  = HexgnTranType("mats_bdy",3,4,5)
            pts_cob   = cob2base*pts_wbase

        return: Transformed BotVec arr object
        """

        if isinstance(tran,SE3): 
            result = self.mat_dot_self(tran)
            return result
        if isinstance(tran,HexgnTranType):
            return self.mats_dot_self(tran)
        else:
            return NotImplemented            
    
    def __add__(self,rght):

        rslt = self.clone()
        if isinstance(rght,BotVec):
            rslt.vec_list = self.vec_list + [rght]
            return rslt
        if isinstance(rght,BotVecArr):
            rslt.vec_list = self.vec_list + rght.vec_list
            return rslt
        else:
            return NotImplemented   
        
    def __getitem__(self, i:int)->BotVec:
        if isinstance(i,int):
            return self.get_ivec(i)
        else: 
            return NotImplemented

    def __setitem__(self,i:int=0,vec:BotVec=None):
        if isinstance(i,int) and isinstance(vec,BotVec):
            return self.set_ivec(i,vec)
        else:
            return NotImplemented     

def test_vec():
    b = BotVec("b",1,2,3)
    t = SE3.Rx(3.14)
    # todo: here
    print(t)
    print(t*b)

def test_vecarr():
    ba = BotVecArr("ba",5)
    t = SE3.Trans(3.14,2,1)
    ca = t*ba
    print(ca)

def test_vecarr2():
    mid = BotVec("mid_leg",1,2,3,0)
    rft = BotVec("rft_leg",1,2,3,1)
    pts_wbase = BotVecArr("ptb",0)
    pts_wbase += mid
    pts_wbase +=rft
    cob2base  = HexgnTranType("mats_bdy",3,4,5)
    pts_cob   = cob2base*pts_wbase

    print(pts_cob)

def test_vecarr_add():
    b = BotVec("b",1,2,3)
    ba = BotVecArr("ba",5)
    print("1:\n"+str(ba))
    ca = ba+b
    print("2:\n"+str(ca))
    print("3:\n"+str(ca+ca))

def test_init_val():
    # a = BotVec()
    # print("1:"+str( a))
    # a = BotVec("bv",x=1,y=2,z=3,i=99)
    # print("2:"+str( a))
    # a = BotVec("bv",[-1,-2,-3],i=98)
    # print("3:"+str( a))
    # a = BotVec("c",[4,5,6],97)
    # print("4:"+str( a))
    # a = BotVec("d",[7,8,9])
    # print("5:"+str( a))

    a = BotVec([17,18,19])
    print(a)

def test_vecar_min():

    mid = BotVec("mid_leg",1,20,3,7)
    rft = BotVec("rft_leg",4,5,6)
    lft = BotVec("lft_leg",[100,-10,-30])
    pts_wbase = BotVecArr("ptb",0)
    pts_wbase = pts_wbase + mid + rft+lft

    min_z =pts_wbase.cmput_lowst_pt('z')
    min_y =pts_wbase.cmput_lowst_pt('y')
    min_x =pts_wbase.cmput_lowst_pt('x')

    print(min_z)
    print(min_y)
    print(min_x)

def test_product():
    a = BotVec("a",[1,0,0])
    b = BotVec("b",[0,1,0])
    c=a.cross_prdct(b)
    d=b.cross_prdct(a)
    print(c)
    print(d)

    e = a*a
    f = b*a
    g = a*3.0
    print(e)
    print(f)
    print(g)

def test_align_vec():
    a = BotVec("a",[1,0,0])
    b = BotVec("b",[0,0,1])
    c=a.align_given_vec(b)
    print(c)
    d = a-b
    print(d)

def test_vecarr_deepcopy():
    a = BotVec("a",[4,5,6],10)
    b = BotVec("b",[1,2,3],11)

    c= BotVec("c",[21,22,23],24)
    ar = BotVecArr("ba",0)
    ar = ar+b
    ar = ar+a
    
    ar2 = deepcopy(ar) 
    ar2[1] = c
    print(ar)
    print(ar2)



    

if __name__ == "__main__":
    #test_vecarr2()
    #test_init_val()
    #test_vecar_min()
    #test_product()
    #test_align_vec()
    print(test_vecarr_deepcopy())