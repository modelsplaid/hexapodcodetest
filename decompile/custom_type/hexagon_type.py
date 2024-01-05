"""
--------------------     
Hexagon's dimension:
--------------------     
 Note1: cob: center of body 
 Note2: f: front length s:side length m: middle length
 
                         
                                 front
                              |-f-|
                              *---*---*--------
                             /   x^    \     |
                            /     |     \    s
                           / y    |      \   |
                 left     *--<---cob------* ---      right            
                           \      |      /|
                            \     |     / |
                             \    |    /  |
                              *---*---*   |
                                  |       |
                                  |---m---|
                        
                                  x axis
                                  ^
                                  |
                                  |
                       y axis<-----
                                cob (origin)

-----------------------------     
Hexagon's coordinate systems:
-----------------------------     
 Hexagon has 9 corner points: 
    right-front  left-front  cob-origin
    right-middle left-middle head-point
    right-back   left-back   tail-point

 Which correspond to 9 coordinate systems, shown below: 
    coord 0: trans cob to right-middle
    coord 1: trans cob to right-front
    coord 2: trans cob to left-front
    coord 3: trans cob to left-middle
    coord 4: trans cob to left-back
    coord 5: trans cob to right-back
    coord 6: trans cob to cob-origin
    coord 7: trans cob to head-point
    coord 8: trans cob to tail-point
     
                                      ^y
                          cor2        |cor1                                 
                          x<--*---*---*-->x
                             /|  y^    \     
                            / V   |     \ ^y   
                           /  y   |   x   \|cor0   
                          *------cob--->--*-->x             
                           \  cor6|      /
                            \     |   ^y/ 
                             \    |   |/cor5  
                              *---*---*-->x   
                                         
"""

import sys
sys.path.append("./")

from    typing          import List, Union
from    spatialmath     import SE3
from    copy            import deepcopy
from    custom_type.bot_cart_type\
                        import BotCartType
import  warnings

class HexgnPtsType:

    __slots__ = ("bdy_pts","name")

    def __init__(self,name=""):
        self.name = name
        self.reset_bdy_pts() 

    def reset_bdy_pts(self):
        """
        Reset body points based on given front,middle,side size
        """   
        self.bdy_pts = {
            0: {"pt": [0, 0, 0], "name":"Body right-middle"},
            1: {"pt": [0, 0, 0], "name":"Body right-front" },
            2: {"pt": [0, 0, 0], "name":"Body left-front"  },
            3: {"pt": [0, 0, 0], "name":"Body left-middle" },
            4: {"pt": [0, 0, 0], "name":"Body left-back"   },
            5: {"pt": [0, 0, 0], "name":"Body right-back"  },
            6: {"pt": [0, 0, 0], "name":"Body cob-origin"  },       
            7: {"pt": [0, 0, 0], "name":"Body head-point"  },      
            8: {"pt": [0, 0, 0], "name":"Body tail-point"  },       
            }
    
    def form_str(self):
        # Format row coord value
        len_pts = self.get_pts_len()
        sr_val_ar = [""]*len_pts

        # Loop over each row
        for j in range(len_pts):
            c_str = "x: ["
            f_str = " y: ["
            t_str = " z: ["

            c     = self.bdy_pts[j]["pt"][0]
            f     = self.bdy_pts[j]["pt"][1]
            t     = self.bdy_pts[j]["pt"][2]

            c_str = c_str + f"{c:+7.2f}"
            f_str = f_str + f"{f:+7.2f}"
            t_str = t_str + f"{t:+7.2f}"

            sr_val_ar[j] = c_str+"]"+f_str+"]"+t_str[0:-1]+"]"

        # Format names    
        sr_nam_ar = [""]*len_pts
        for j in range(len_pts): # Fixe name length

            sr_nam_ar[j] = self.bdy_pts[j]["name"]
            if(len(sr_nam_ar[j])<18):
                sr_nam_ar[j] = sr_nam_ar[j] +" "*(18-len(sr_nam_ar[j]))
            sr_nam_ar[j] = sr_nam_ar[j] + sr_val_ar[j] +"\n"

        # Append each row
        full_str = ""
        for j in range(len_pts):
            full_str = full_str + sr_nam_ar[j]
        full_str = self.name+": \n"+full_str

        return full_str

    def clone(self):
        """
        Clone a copy of self-object 
        """
        cls         = self.__class__
        result      = cls.__new__(cls)

        # copy value 
        result.name    = deepcopy(self.name)
        result.bdy_pts = deepcopy(self.bdy_pts)

        return result    
    
    def mat_dot_self(self,tran_cob:SE3):
        """
        Given translation matrix , update hexagon coordinates respectively 
        e.g: tran_cob*bdy_pts[0]
             tran_cob*bdy_pts[1]
             tran_cob*bdy_pts[2]
             ...
        Param : tran_cob: Given tans matrix
        return: Transformed HexgnTranType object
        """

        result = self.clone()
        # Translate matrices
        for key in self.bdy_pts:

            pt = tran_cob*self.get_pts(key)
            result.set_pts(key, [pt[0][0],pt[1][0],pt[2][0]])

        # copy value 
        result.name = "trans from " +self.name
        return result


    def set_pts(self,i=0,xyz=[0,0,0]):
        """
        Param i  : i= 0--8, the key 
        Param xyz: [x,y,z]
        """
        self.bdy_pts[i]["pt"][0] = xyz[0]
        self.bdy_pts[i]["pt"][1] = xyz[1]
        self.bdy_pts[i]["pt"][2] = xyz[2]
    
    def set_name(self,name:str):
        self.name = name
    
    def get_pts(self,i=0):
        """
        Param i : i= 0--8, the key 
        Return  : [x,y,z]
        """
        xyz = deepcopy(self.bdy_pts[i]["pt"])
        return xyz 
    
    def get_name(self):
        return self.name 

    def get_pts_len(self):
        return len(self.bdy_pts)



    def __str__(self):
        full_str = self.form_str()
        return full_str

    def __rmul__(self,tran_cob:SE3):
        """
        Update body points given transformation mat
        Param : tran_cob: Given tans matrix
        return: Transformed HexgnTranType object
        """

        if isinstance(tran_cob,SE3): 
            result = self.mat_dot_self(tran_cob)
            return result
        else:
            return NotImplemented 

    def __getitem__(self, key:int)->List[Union[float,float,float]]:
        """
        Given key index, return list of [x,y,z]
        """
        if isinstance(key,int) and key >=0 and key <  len(self.bdy_pts):
            pt = self.get_pts(key)
            return pt
        else: 
            warnings.warn("Failed to get value")
            return ([0,0,0])
    
    def __setitem__(self,key:int=0,pt:List[Union[float,float,float]]=[0,0,0]):
        """
        Given key index and [x,y,z], set point
        """
        if isinstance(key,int) and key >=0 and key < len(self.bdy_pts):
            self.set_pts(key,pt)
            return True
        else: 
            warnings.warn("Failed to set value")
            return False  
                
class HexgnTranType:
    __slots__ = ("name","mat_bdy_cords","f", "m", "s")
    """
    mat_bdy_cords: Transformation matrix to body coordinates
    tran_cob_cord : Transformation matrix to center-of-body coordinates
    """             

    def __init__(self,name="",f=0,m=0,s=0,coxa_rot:List=[-90,-90,90,90,90,-90]):
        """
        :param f,m,s    : Hexagons front,middle,side size 

        :param coxa_rot: Define each leg's coxa-z-axis rotation shift angle(deg).  
        :type  coxa_rot: A list in the format of :
                          coxa_rot[0]: right-middle coxa_rot[1]: right-front coxa_rot[2]: left-front 
                          coxa_rot[3]: left-middle  coxa_rot[4]: left-back   coxa_rot[5]: right-back
        
        """

        self.name = name
        self.set_trans_arr(f,m,s,coxa_rot)

    def clone(self):
        """
        Clone a copy of self-object 
        """
        cls         = self.__class__
        result      = cls.__new__(cls)

        # copy value 
        result.mat_bdy_cords\
                    = deepcopy(self.mat_bdy_cords)
        
        result.name = deepcopy(self.name)
        result.f    = deepcopy(self.f)
        result.m    = deepcopy(self.m)
        result.s    = deepcopy(self.s)

        return result
    
    def inv(self):
        """
        Inverse body transformation, and return a new one 
        """
        result = self.clone()
        result.name = "inv from "+ self.name

        for key in self.mat_bdy_cords:
            result.mat_bdy_cords[key]["T"] = self.mat_bdy_cords[key]["T"].inv()

        return result 
    
    def mat_dot_self(self,tran_cob:SE3):
        """
        Update by given transformation matrix from 

        Param : tran_cob: Given tans matrix
        return: Transformed  object
        """

        result = self.clone()
        # Translate matrices
        for key in self.mat_bdy_cords:
            result.mat_bdy_cords[key]["T"] = tran_cob*self.mat_bdy_cords[key]["T"]

        # copy value 
        result.name = "trans from " +self.name
        return result
    
    def self_dot_mat(self,tran_cob:SE3):
        """
        Update by given transformation matrix from 

        Param : tran_cob: Given tans matrix
        return: Transformed  object
        """
        result = self.clone()

        # Translate matrices
        for key in self.mat_bdy_cords:
           result.mat_bdy_cords[key]["T"] = self.mat_bdy_cords[key]["T"]*tran_cob

        result.name = "trans from " +self.name
        return result
        
    def self_dot_pts(self,bdy_pts:HexgnPtsType):
        """
        Transform all hexagon points. 
        eg.:
            bdy_pts  = HexgnPtsType("bdy_pts")
            mats_bdy = HexgnTranType("mats_bdy",3,4,5)
            bdy_pts2_wrt_cob = mats_bdy*bdy_pts
        """
        
        # Loop over all pts
        new_bdy_pts = HexgnPtsType("new_bdy_pts")
        new_bdy_pts.set_name("Trans pts from " + bdy_pts.get_name())

        for i in range(bdy_pts.get_pts_len()):
            arr = self.mat_bdy_cords[i]["T"] * bdy_pts[i]

            new_bdy_pts.set_pts(i,[arr[0][0],arr[1][0],arr[2][0]])

        return new_bdy_pts 

    def self_dot_cart_type(self,leg_cart:BotCartType):
        """
        Transform all leg points in type of BotCartType. 
        eg.:
            leg_pts = BotCartType("leg")
            mats_bdy = HexgnTranType("hgd",3,4,5)
            legs_wrt_cob = mats_bdy*leg_pts
        """

        # Loop over all pts
        new_leg_pts      = BotCartType("new_leg_pts")
        new_leg_pts.name = "Trans pts from " + leg_cart.name

        for i in range(new_leg_pts.get_num_legs()):
            arr = self.mat_bdy_cords[i]["T"] * leg_cart.get_pt_by_idx(i)
            new_leg_pts.set_by_leg_idx(i,[arr[0][0],arr[1][0],arr[2][0]])

        return new_leg_pts 


    def set_trans_arr(self,f=0,m=0,s=0,coxa_rot:List =[-90,-90,90,90,90,-90]):
        """
        :param f,m,s    : Hexagons front,middle,side size 

        :param coxa_rot: Define each leg's coxa-z-axis rotation shift angle(deg).  
        :type  coxa_rot: A list in the format of :
                          coxa_rot[0]: right-middle coxa_rot[1]: right-front coxa_rot[2]: left-front 
                          coxa_rot[3]: left-middle  coxa_rot[4]: left-back   coxa_rot[4]: right-back
        
        """
                
        self.f = deepcopy(f)
        self.m = deepcopy(m)
        self.s = deepcopy(s) 

        # todo: here change 180 from outside 
        xgon_cfg= {
            0: {"transl": [ 0,-m, 0],"rot_rpy":[0, 0,coxa_rot[0]], "name":"cob to right-middle"},
            1: {"transl": [ s,-f, 0],"rot_rpy":[0, 0,coxa_rot[1]], "name":"cob to right-front" },
            2: {"transl": [ s, f, 0],"rot_rpy":[0, 0,coxa_rot[2]], "name":"cob to left-front"  },
            3: {"transl": [ 0, m, 0],"rot_rpy":[0, 0,coxa_rot[3]], "name":"cob to left-middle" },
            4: {"transl": [-s, f, 0],"rot_rpy":[0, 0,coxa_rot[4]], "name":"cob to left-back"   },
            5: {"transl": [-s,-f, 0],"rot_rpy":[0, 0,coxa_rot[5]], "name":"cob to right-back"  },
            6: {"transl": [ 0, 0, 0],"rot_rpy":[0, 0,          0], "name":"cob to cob-origin"  },       
            7: {"transl": [ s, 0, 0],"rot_rpy":[0, 0,          0], "name":"cob to head-point"  },      
            8: {"transl": [-s, 0, 0],"rot_rpy":[0, 0,          0], "name":"cob to tail-point"  }}
        
        self.mat_bdy_cords = {
            0: {"T": SE3(), "name":"coord 0 T_right-middle"},
            1: {"T": SE3(), "name":"coord 1 T_right-front" },
            2: {"T": SE3(), "name":"coord 2 T_left-front"  },
            3: {"T": SE3(), "name":"coord 3 T_left-middle" },
            4: {"T": SE3(), "name":"coord 4 T_left-back"   },
            5: {"T": SE3(), "name":"coord 5 T_right-back"  },
            6: {"T": SE3(), "name":"coord 6 T_cob-origin"  },       
            7: {"T": SE3(), "name":"coord 7 T_head-point"  },      
            8: {"T": SE3(), "name":"coord 8 T_tail-point"  }}
        
        for key in self.mat_bdy_cords:
            tran = xgon_cfg[key]["transl" ]
            rpy  = xgon_cfg[key]["rot_rpy"]

            R = SE3.RPY(rpy[0],rpy[1],rpy[2],unit="deg", order='zyx')
            T = SE3.Trans(tran[0],tran[1],tran[2])
            self.mat_bdy_cords[key]["T"] = T*R
    
    def set_mat_bdy_mat(self,i,tran_mat:SE3):
        """
        Given key index, and transformation matrix
        """
        self.mat_bdy_cords[i]["T"] = tran_mat

    def get_mat_bdy_mat(self,i)->SE3:
        """
        Given key index, return SE3() transformation matrix
        """
        return self.mat_bdy_cords[i]["T"]

    def __rmul__(self,tran_cob:SE3):
        """
        Update by given transformation matrix from 

        Param : tran_cob: Given tans matrix
        return: Transformed  object
        """
        if isinstance(tran_cob,SE3): 
            result = self.mat_dot_self(tran_cob)
            return result
        else:
            return NotImplemented 

    def __mul__(self, right):

        """
        Case 1:  SE3 type:
                    Given translation matrix from cob to gnd, update hexagon coordinates respectively. 
                    e.g: 
                        mat_bdy     = HexgnTranType("hgd",3,4,5)
                        mat_gnd2cob = SE3.Trans(0,0,10)
                        mat_gnd2bdy = mat_bdy*mat_gnd2cob

        Case 2: HexgnPtsType type:
                    bdy_pts         = HexgnPtsType("bdy_pts")
                    mats_bdy        = HexgnTranType("mats_bdy",3,4,5)
                    bdy_pts_wrt_cob = mats_bdy*bdy_pts

        Case 3: BotCartType type:
                    leg_pts         = BotCartType("leg")
                    mats_bdy        = HexgnTranType("hgd",3,4,5)
                    legs_wrt_cob    = mats_bdy*leg_pts
        """

        if isinstance(right,SE3): 
            result = self.self_dot_mat(right)

        elif isinstance(right,HexgnPtsType): 
            result = self.self_dot_pts(right)
        
        elif isinstance(right,BotCartType): 
            result = self.self_dot_cart_type(right)
        else: 
            return NotImplemented 
        
        return result

    def __getitem__(self, key:int)->SE3:
        """
        Given key index, return SE3() transformation matrix
        """

        if isinstance(key,int) and key >=0 and key <  len(self.mat_bdy_cords):
            tran = self.get_mat_bdy_mat(key)
            return tran
        else: 
            warnings.warn("Failed to get value")
            return SE3()

    def __setitem__(self,key:int,tran:SE3):
        """
        Given key index, return SE3() transformation matrix
        """
        if isinstance(key,int) and key >=0 and key <  len(self.mat_bdy_cords):
            self.set_mat_bdy_mat(key,tran)
            return True
        else: 
            warnings.warn("Failed to set value")
            return False 

    def __str__(self):
        gstr= self.name+":\n"

        for key in self.mat_bdy_cords:
            nstr = self.mat_bdy_cords[key]["name"]
            tstr = str(self.mat_bdy_cords[key]["T"   ])

            gstr = gstr + nstr + ": \n" + tstr +"\n"
        return gstr 
    
def test_trans_mat():
    hgd = HexgnTranType("hgd",3,4,5)

    gnd_t_cob = SE3.Rz(180,unit="deg")
    t_hgd = hgd.mat_dot_self(gnd_t_cob)

    print(hgd)
    print(t_hgd)

def test_bdy_pts():
    tran_cob2xgn = HexgnTranType("hgd",3,4,5)

    bdy = HexgnPtsType("bdy")
    bdy_pts_cob = tran_cob2xgn.self_dot_pts(bdy)

    mat_gnd2cob = SE3.Trans(0,0,10)
    tran_gnd2xgn= tran_cob2xgn.mat_dot_self(mat_gnd2cob)
    bdy_pts_gnd = tran_gnd2xgn.self_dot_pts(bdy)
    print(bdy)
    print(bdy_pts_cob)
    print(bdy_pts_gnd)

def test_matdotself_rmul():
    mat_bdy     = HexgnTranType("hgd",3,4,5)
    mat_gnd2cob = SE3.Trans(0,0,10)
    mat_gnd2bdy = mat_gnd2cob*mat_bdy

    print(mat_gnd2bdy)

def test_selfdotmat_mul():
    mat_bdy     = HexgnTranType("hgd",3,4,5)
    mat_gnd2cob = SE3.Trans(0,0,10)
    mat_gnd2bdy = mat_bdy*mat_gnd2cob

    print(mat_gnd2bdy)
    print(mat_bdy)

def test_selfdotpts_mul():
    bdy_pts = HexgnPtsType("bdy")

    mats_bdy = HexgnTranType("hgd",3,4,5)
    bdy_pts2_wrt_cob = mats_bdy*bdy_pts

    #print(mats_bdy)
    print(bdy_pts2_wrt_cob)

def test_selfdotcart_mul():
    leg_pts = BotCartType("leg")
    mats_bdy = HexgnTranType("hgd",3,4,5)
    legs_wrt_cob = mats_bdy*leg_pts

    #print(mats_bdy)
    print(legs_wrt_cob)

def test_inv():
    mats_bdy = HexgnTranType("mats_bdy",3,4,5)
    inv_mat_bdy = mats_bdy.inv()
    print(mats_bdy)
    print(inv_mat_bdy)

if __name__ == "__main__":
    #test_matdotself_rmul()
    #test_selfdotmat_mul()
    #test_selfdotpts_mul()
    #test_selfdotcart_mul()
    test_inv()