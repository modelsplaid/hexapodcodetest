import json 
import sys
sys.path.append("../")
from collections                import deque
from copy                       import deepcopy
from typing                     import List, Union

from spatialmath                import SE3
from custom_type.bot_cart_type  import BotCartType
from custom_type.bot_base_type  import BotBaseType
from custom_type.hexagon_type   import HexgnTranType

class CarSqsType(BotBaseType):   

    __slots__ = ("name","ctraj_dq","leg_sz","_iter_idx_")
    
    def __init__(self, name=None,**kwds):
        """
         Case1: 
               Init by given a dictionary: 
               ct1 = CarSqsType(name="ct1",ctraj_dic=ctraj_dict)
         Case2: 
               Init as empty trajectory:
               ct1 = JTrajType(name="ct1")
               
         Case3:Init by specify initial value and trajectory length
               ct1 = CTrajType(name="ct1",init_val=val,traj_len=len)
        
        ctraj_dict type: 
        {
        0: {"x": [t1...tn],"y": [t1...tn],"z": [t1...tn],"name": "right-middle","id": 0},
        1: {"x": [t1...tn],"y": [t1...tn],"z": [t1...tn],"name": "right-front" ,"id": 1},
        2: {"x": [t1...tn],"y": [t1...tn],"z": [t1...tn],"name": "left-front"  ,"id": 2},
        3: {"x": [t1...tn],"y": [t1...tn],"z": [t1...tn],"name": "left-middle" ,"id": 3},
        4: {"x": [t1...tn],"y": [t1...tn],"z": [t1...tn],"name": "left-back"   ,"id": 4},
        5: {"x": [t1...tn],"y": [t1...tn],"z": [t1...tn],"name": "right-back"  ,"id": 5}
        }
        """
        
        self.ctraj_dq = deque()# A dequeue of BotCartType
        self.leg_sz = super().LEG_SZ
        #print("self.leg_sz:",self.leg_sz)
        # Case 1: Init by given a dictionary:
        if len(kwds.keys())==1 and list(kwds.keys())[0]=="ctraj_dic":
            self.name  = name
            ctraj_dic = deepcopy(kwds["ctraj_dic"])
            self.conv_apnd_dic2dq(ctraj_dic)
            self.conv_dq2dic()
            return 
        
        # Case 2: Init as empty trajectory.
        elif len(kwds.keys())==0:

            self.name  = name
            return 
        
        # Case 3: Init Init by specify initial value and trajectory length.
        elif len(kwds.keys())==2 and isinstance(kwds["traj_len"],int): 
            init_val = kwds["init_val"]
            traj_len = kwds["traj_len"]
            ctraj_tmplt = \
                {
                0: {"x": [init_val]*traj_len,"y": [init_val]*traj_len,"z": [init_val]*traj_len,"name": "right-middle","id": 0},
                1: {"x": [init_val]*traj_len,"y": [init_val]*traj_len,"z": [init_val]*traj_len,"name": "right-front" ,"id": 1},
                2: {"x": [init_val]*traj_len,"y": [init_val]*traj_len,"z": [init_val]*traj_len,"name": "left-front"  ,"id": 2},
                3: {"x": [init_val]*traj_len,"y": [init_val]*traj_len,"z": [init_val]*traj_len,"name": "left-middle" ,"id": 3},
                4: {"x": [init_val]*traj_len,"y": [init_val]*traj_len,"z": [init_val]*traj_len,"name": "left-back"   ,"id": 4},
                5: {"x": [init_val]*traj_len,"y": [init_val]*traj_len,"z": [init_val]*traj_len,"name": "right-back"  ,"id": 5}
                }   
            self.conv_apnd_dic2dq(ctraj_tmplt)
            self.conv_dq2dic()
            self.name  = name
            return 
    
    def conv_apnd_dic2dq(self,ctraj_dic:dict=None):
        """
        Convert dictionary type  and append to dequeue type trajectory
        ctraj_dic = \
        {
        0: {"x": [t1...tn],"y": [t1...tn],"z": [t1...tn],"name": "right-middle","id": 0},
        1: {"x": [t1...tn],"y": [t1...tn],"z": [t1...tn],"name": "right-front" ,"id": 1},
        2: {"x": [t1...tn],"y": [t1...tn],"z": [t1...tn],"name": "left-front"  ,"id": 2},
        3: {"x": [t1...tn],"y": [t1...tn],"z": [t1...tn],"name": "left-middle" ,"id": 3},
        4: {"x": [t1...tn],"y": [t1...tn],"z": [t1...tn],"name": "left-back"   ,"id": 4},
        5: {"x": [t1...tn],"y": [t1...tn],"z": [t1...tn],"name": "right-back"  ,"id": 5}
        }
        """
        for j in range(len(ctraj_dic[0]["x"])):
            bc = BotCartType(name='csq'+str(j))
            for i in range(bc.get_num_legs()):
                x = ctraj_dic[i]["x"][j]
                y = ctraj_dic[i]["y"][j]
                z = ctraj_dic[i]["z"][j]
                bc.set_by_leg_idx(i,[x,y,z])
            self.ctraj_dq.append(bc)

    def conv_dq2dic(self)->dict:
        """
        Convert self.ctraj_dq (dequeue type) trajectory to dictionary list type 
        
        return type: 
        ctraj_dic = \
        {
        0: {"x": [t1...tn],"y": [t1...tn],"z": [t1...tn],"name": "right-middle","id": 0},
        1: {"x": [t1...tn],"y": [t1...tn],"z": [t1...tn],"name": "right-front" ,"id": 1},
        2: {"x": [t1...tn],"y": [t1...tn],"z": [t1...tn],"name": "left-front"  ,"id": 2},
        3: {"x": [t1...tn],"y": [t1...tn],"z": [t1...tn],"name": "left-middle" ,"id": 3},
        4: {"x": [t1...tn],"y": [t1...tn],"z": [t1...tn],"name": "left-back"   ,"id": 4},
        5: {"x": [t1...tn],"y": [t1...tn],"z": [t1...tn],"name": "right-back"  ,"id": 5}
        }
        """
        len_sqs = len(self.ctraj_dq)
        ctraj_dic = \
            {
            0: {"x": [0]*len_sqs,"y": [0]*len_sqs,"z": [0]*len_sqs,"name": "right-middle","id": 0},
            1: {"x": [0]*len_sqs,"y": [0]*len_sqs,"z": [0]*len_sqs,"name": "right-front" ,"id": 1},
            2: {"x": [0]*len_sqs,"y": [0]*len_sqs,"z": [0]*len_sqs,"name": "left-front"  ,"id": 2},
            3: {"x": [0]*len_sqs,"y": [0]*len_sqs,"z": [0]*len_sqs,"name": "left-middle" ,"id": 3},
            4: {"x": [0]*len_sqs,"y": [0]*len_sqs,"z": [0]*len_sqs,"name": "left-back"   ,"id": 4},
            5: {"x": [0]*len_sqs,"y": [0]*len_sqs,"z": [0]*len_sqs,"name": "right-back"  ,"id": 5}
            }   
        
        for j in range(len(self.ctraj_dq)):

            bc = self.ctraj_dq[j] # loop over BotCartType() dequeue data
            for i in range(bc.get_num_legs()):
                [x,y,z] = bc[i]
                ctraj_dic[i]["x"][j] = x
                ctraj_dic[i]["y"][j] = y
                ctraj_dic[i]["z"][j] = z
        ctraj_dic = ctraj_dic
        return ctraj_dic

    def key_str2int(self,str_key_dic):
        '''
        After json.load(out_file), json does not support int type key in dictionary, 
        so I created this function to do that.

        :param str_key_dic : A dictionary which its' key is a str(int) type
        :type  str_key_dic : Dictionary 
        
        :return int_key_dic: A dictionary which its' key is a int type 
        :type   int_key_dic: Dictionary 
        '''
    
        int_key_dic = dict()
        for strkey in str_key_dic:
            int_key_dic[int(strkey)] = str_key_dic[strkey]
        return int_key_dic

    def pop_fnt_fram(self)->BotCartType:
        """
        Pop out one frame from front. 
        Return None if length == 0
        """

        if self.get_traj_len() == 0: 
            return None 
        return self.ctraj_dq.popleft()  

    def appnd_cpose(self,cpose:BotCartType):
        """
        Given a cpose type value, append cpose to tail
        """

        self.ctraj_dq.append(deepcopy(cpose))

    def clear_dq(self):
        """
        Clear dequeue buffer 
        """
        self.ctraj_dq.clear()


    def clone(self):
        """
        Clone a copy of self-object 
        """
        cls         = self.__class__
        result      = cls.__new__(cls)

        # copy value 
        result.ctraj_dq = deepcopy(self.ctraj_dq )
        result.name     = deepcopy(self.name     )
        result.leg_sz   = deepcopy(self.leg_sz   )

        return result

    def mat_dot_self(self,trans:SE3):
        """
        Given translation matrix , update legs' points respectively 
        e.g: tran*T_right-middle
             tran*T_right-front
             tran*T_left-front
             ...

        Param : tran_cob: Given tans matrix
        return: Transformed CtrajType object
        """
        result = self.clone()
        # Translate matrices
        for traj_idx in range(self.get_traj_len()):
            one_pose = self[traj_idx]
            result[traj_idx] = trans*one_pose

        # copy value 
        result.name = "trans from " +self.name+": "
        return result
    
    def mats_dot_self(self,trans:HexgnTranType):
        """
        Given HexgnTranType matrices , update legs' points respectively 
        e.g: tran*T_right-middle
             tran*T_right-front
             tran*T_left-front
             ...
        """
        result = self.clone()
        
        # Translate matrices
        for traj_idx in range(self.get_traj_len()):
            one_pose = self[traj_idx]
            result[traj_idx] = trans*one_pose

        # copy value 
        result.name = "trans from " +self.name+": "
        return result
     
    def print_table(self,keep_old=False):
        """
        Print message in a table form
        Param keep_old: =True : When scroll up terminal, will see old record
                        =False: No record
        """

        hom_pos  = '\033[H'
        clr_str  = '\033[2J'

        # Move curser to origin reference: https://github.com/gravmatt/py-term

        if keep_old == True:
            sys.stdout.write(clr_str)

        sys.stdout.write(hom_pos)
        sys.stdout.flush()

        apend_str = self.form_str()
        sys.stdout.write(apend_str)
        sys.stdout.flush()   


    def form_str(self):
        ctraj_dic = self.conv_dq2dic()

        # Format row coord value
        len_arr  = len(ctraj_dic[0]["x"])
        len_legs = len(ctraj_dic)
        sr_val_ar = [""]*len_legs

        # Loop over each row
        for j in range(len_legs):
            x_str = "x: ["
            y_str = " y: ["
            z_str = " z: ["
            for i in range(len_arr):
                x = ctraj_dic[j]["x"][i]
                y = ctraj_dic[j]["y"][i]
                z = ctraj_dic[j]["z"][i]

                x_str = x_str + f"{x:+8.2f},"
                y_str = y_str + f"{y:+8.2f},"
                z_str = z_str + f"{z:+8.2f},"

            sr_val_ar[j] = x_str+"],"+y_str+"],"+z_str[0:-1]+"]"

        # Format names
        sr_nam_ar = [""]*len_legs
        for j in range(len_legs): # Fixe namne length

            sr_nam_ar[j] = ctraj_dic[j]["name"]
            if(len(sr_nam_ar[j])<13):
                sr_nam_ar[j] = sr_nam_ar[j] +" "*(13-len(sr_nam_ar[j]))
            sr_nam_ar[j] = sr_nam_ar[j] + "coords: "+ sr_val_ar[j] +"\n"

        # Append each row
        full_str = ""
        for j in range(len_legs):
            full_str = full_str + sr_nam_ar[j]
            
        full_str = self.name+": \n"+full_str
        return full_str

    def cpos_is_in(self,cpos:BotCartType=None)->bool:
        """
        Check if given cpos is in this sequence
        """
        for onepos in self:
            if(onepos == cpos):
                return True
        return False

    def get_traj_ileg(self,leg_id:int=0)->List:
        '''
        Given legid, return [[x1,x2,...xn],[y1,y2,...yn],[z1,z2,...z3]]
        '''
        ctraj_dic = self.conv_dq2dic()
        x_lst = deepcopy(ctraj_dic[leg_id]['x'])
        y_lst = deepcopy(ctraj_dic[leg_id]['y'])
        z_lst = deepcopy(ctraj_dic[leg_id]['z'])

        return [x_lst,y_lst,z_lst]

    def get_cpose_by_jname(self,jname:str = "tibia")->BotCartType:
        """
        Given a joint name, return coordinates for all legs' for that joint
        In order use this function, user has to make sure that: 
        self.ctraj_dq[0]: stores base's  cartesian coordinate   
        self.ctraj_dq[1]: stores coxa's  cartesian coordinate   
        self.ctraj_dq[2]: stores femur's cartesian coordinate   
        self.ctraj_dq[3]: stores tibia's cartesian coordinate   

        Param: jname : joint name.
                       Possible choises: ,"coxa","base","femur","tibia"
        """

        if jname == "base" :
            return self.get_one_cpose_fram(0)   
        
        if jname == "coxa" :
            return self.get_one_cpose_fram(1)   
        
        if jname == "femur":
            return self.get_one_cpose_fram(2)
         
        if jname == "tibia":
            return self.get_one_cpose_fram(3)
        
    def get_one_cpose_fram(self,traj_idx:int)->BotCartType:
        """
        Given a trajectory index, return poses for every leg

        """
        one_cpos = deepcopy(self.ctraj_dq[traj_idx])
        return one_cpos

    def get_traj_len(self): 
        # Return the length of the trajectories 
        return len(self.ctraj_dq)
    
    def get_num_legs(self):
        return self.leg_sz
    
    def get_ctraj_dic(self):
        ctraj_dic = self.conv_dq2dic()
        return ctraj_dic

    def get_one_pt(self,leg_idx,traj_idx)->List[Union[float,float,float]]:
        ctraj_dic = self.conv_dq2dic()
        x = deepcopy(ctraj_dic[leg_idx]["x"][traj_idx])
        y = deepcopy(ctraj_dic[leg_idx]["y"][traj_idx])
        z = deepcopy(ctraj_dic[leg_idx]["z"][traj_idx])

        return [x,y,z]
    
    def get_name(self):
        return self.name 
    
    def get_redunt_mov_ids(self)->List:
        """
        Get redundant moving indices. 
        Redundant mov: Swing distance is zero (mark time)
        """
        gnd_ids = []
        for iseq,one_cp in enumerate(self):
            if one_cp.is_all_gnd():
                gnd_ids = gnd_ids + [iseq]

        redun_pos_ids = []
        for i in range(len(gnd_ids)-1):
            i0 = gnd_ids[i]
            i1 = gnd_ids[i+1]

            if self[i0]-self[i1]<0.1: # For round-off error
                for j in range(i0,i1):
                    redun_pos_ids = redun_pos_ids +[j]
        
        return redun_pos_ids
                
    def set_name(self,name=""):
        self.name = name
         
    def set_dq(self,dq:deque):
        """
        Given a trajectory queue.
        """
        self.ctraj_dq = dq
        self.conv_dq2dic()
        
    def set_one_cpose_fram(self,traj_idx:int,cpose:BotCartType):
        """
        Given a cpose for each leg and an index. Set the cpose to trajectory
        """

        for leg_idx in range(self.leg_sz):
            [x,y,z] = cpose.get_pt_by_idx(leg_idx)
            self.set_one_pt(leg_idx,traj_idx,deepcopy([x,y,z]))

    def set_by_strkey(self,json_str):
        '''
        Json file does not support int key, Convert to int key. 
        '''
        
        self.clear_dq()
        ctraj_dic = self.key_str2int(json_str)
        self.conv_apnd_dic2dq(ctraj_dic)
        self.conv_dq2dic()

    def set_one_pt(self,leg_idx,traj_idx,*args,**kwds):
        '''
         Arguments: 
         case 1: *args is pt=[0,0,0]
         case 2: **kwds choises are:  x=number, y=number,z=number
        
         Example1 set a point: 
               ct1 = CarTraj(name="ct1")
               ct1.set_one_pt(0,0,[1,2,3])
               print("arr"+str(ct1.get_one_pt(0,0)))
        
         Example2 set a point by specifying one or more axis: 
               ct1.set_one_pt(1,0,x=9,y=8,z=7)
               print("separate"+str(ct1.get_one_pt(1,0)))
               
               ct1.set_one_pt(3,2,x=99,y=88)
               print("separate"+str(ct1.get_one_pt(3,2)))
        '''
        # case 1
        if len(args) == 1 and isinstance(args[0], list):
            ccart = self.ctraj_dq[traj_idx]
            ccart.set_by_leg_idx(leg_idx,[args[0][0],args[0][1],args[0][2]])
            self.ctraj_dq[traj_idx] = ccart
            return 
        
        # case 2
        if len(args) == 0 and len(kwds.keys()) > 0:
            for axis_name in kwds.keys(): # keys are any from : 'x' , 'y' , 'z' 
                ccart = self.ctraj_dq[traj_idx]
                ccart.set_by_ct_nam(leg_idx,axis_name,kwds[axis_name])
                self.ctraj_dq[traj_idx] = ccart
            return
        
        raise NameError('fatal error: Incorrect arguments')
            
    def iadd (self,d):
        """
        Append to current trajectory given CarSqsType or BotCartType
        Case1 : 
            ct1 = BotCartType("ct1",dic_tmplt)
            cj1 = CarSqsType(name="cj1")
            cj2 += ct1, cj2 is a copy of cj1 

        Case2 : 
            cj0 = CarSqsType(name="cj0")
            cj1 = CarSqsType(name="cj1")
            cj1 += cj1+cj0 
        """

        self.ctraj_dq = self.__add__(d)    

    def __add__(self,e):
        """
        Append to current trajectory given CarSqsType or BotCartType
        Case1 : 
            ct1 = BotCartType("ct1",dic_tmplt)
            cj1 = CarSqsType(name="cj1")
            cj2 = cj1+ct1, cj2 is a copy of cj1 

        Case2 : 
            cj0 = CarSqsType(name="cj0")
            cj1 = CarSqsType(name="cj1")
            cj2 = cj1+cj0 
        """
        d = deepcopy(e)
        if isinstance(d,CarSqsType): 
            # Reload the add("+") sign, as append operation
            ctraj_dq = deepcopy(self.ctraj_dq)
            
            for j in range(len(d)):
                ctraj_dq.append(d[j]) 
            apnd_ctraj = CarSqsType(name="appended traj")
            apnd_ctraj.set_dq(ctraj_dq)
            return apnd_ctraj
        
        elif isinstance(d,BotCartType):
            ctraj_dq = deepcopy(self.ctraj_dq)
            ctraj_dq.append(d)
            apnd_ctraj = CarSqsType(name="appended traj")
            apnd_ctraj.set_dq(ctraj_dq)
            return apnd_ctraj
        else: 
            return NotImplemented
      
    def __rmul__(self,tran):
        """
        Given translation matrix from gnd to cob, update hexagon coordinates respectively 
            e.g: 
                traj_pts    = CTrajType("traj_pts")
                mat_gnd2cob = SE3.Trans(0,0,10)
                pts_gnd2bdy = mat_gnd2cob*traj_pts
        Param : tran: Given tans matrix
        return: Transformed CTrajType object
        """
        if isinstance(tran,SE3): 
            result = self.mat_dot_self(tran)
            return result
        elif isinstance(tran,HexgnTranType):
            result = self.mats_dot_self(tran)
            return result
        else:
            return NotImplemented         
    
    def __iter__(self):
        self._iter_idx_ = 0
        return self    
    
    def __next__(self)->BotCartType:
        if self._iter_idx_ < self.get_traj_len():
            one_cp = self.ctraj_dq[self._iter_idx_]
            self._iter_idx_ += 1
            return one_cp
        else:
            raise StopIteration
        
    def __eq__(self, robj)->bool:

        if isinstance(robj,CarSqsType): 
            if self.get_traj_len() != robj.get_traj_len():
                return False
            
            for i,frame in enumerate(robj):
                if self.get_traj_len() != robj.get_traj_len():
                    return False
                if self.get_one_cpose_fram(i) != frame:
                    return False
            return True
        
        else:
            return NotImplemented 

    def __str__(self):
        return self.form_str()
    
    def __setitem__(self,traj_idx:int,cpose:BotCartType):
        return self.set_one_cpose_fram(traj_idx,cpose)

    def __getitem__(self, traj_idx:int)->BotCartType:
        """
        Given a trajectory index, return a frame of cpose 
        """
        return self.get_one_cpose_fram(traj_idx)

    def __len__(self):
        """
        Get trajectory length  
        return [trajectory_length]
        """
        return self.get_traj_len()

def dq_test_CarTraj():

    # Test set and get pt 
    ctraj_tmplt = \
        {
        0: {"x": [195 ,195 ,195 , 195],"y": [ -30, -30,  30,  30],"z": [10,0,0,10],"name": "right-middle","id": 0},
        1: {"x": [161 ,161 ,161 , 161],"y": [  89,  89, 149, 149],"z": [10,0,0,10],"name": "right-front" ,"id": 1},
        2: {"x": [-161,-161,-161,-161],"y": [ 149, 149,  89,  89],"z": [10,0,0,10],"name": "left-front"  ,"id": 2},
        3: {"x": [-195,-195,-195,-195],"y": [  30,  30, -30, -30],"z": [10,0,0,10],"name": "left-middle" ,"id": 3},
        4: {"x": [-161,-161,-161,-161],"y": [ -88,-88 ,-148,-148],"z": [10,0,0,10],"name": "left-back"   ,"id": 4},
        5: {"x": [161 ,161 ,161 , 161],"y": [-149,-149, -89, -89],"z": [10,0,0,10],"name": "right-back"  ,"id": 5}
        }
    ct1 = CarSqsType(name="ct1",ctraj_dic = ctraj_tmplt)

    ct1.set_one_pt(0,0,[1,2,3])
    print("arr"+str(ct1.get_one_pt(0,0)))
    
    ct1.set_one_pt(1,0,x=9,y=8,z=7)
    print("separate"+str(ct1.get_one_pt(1,0)))

    ct1.set_one_pt(3,2,x=99,y=88)
    print("separate"+str(ct1.get_one_pt(3,2)))
    
    # Test Appending ctraj
    ct2 = CarSqsType(name="ct2",ctraj_dic = ctraj_tmplt)
    print(str(ct1+ct2)+"name: "+(ct1+ct2).name )
    
    # Test appending ctype
    bc = BotCartType()
    ct3 = ct2+bc
    print(ct3)
 
def dq_test_load_json():
    
    ct1 = CarSqsType()
    out_file = open("../config/ctraj_sqs_tright.json", "r") 
    trght_gaits = json.load(out_file)
    pseqs = trght_gaits["CTRAJ_TMPLT_WRT_GND"]
    ct1 = CarSqsType("tr tmplt")
    
    ct1.set_by_strkey(pseqs)

    s1 = ct1[0]
    print(ct1)
    print(s1)

def dq_test_add_override():
    # Test set and get pt 
    ctraj_tmplt = \
        {
        0: {"x": [195 ,195 ,195 , 195],"y": [ -30, -30,  30,  30],"z": [10,0,0,10],"name": "right-middle","id": 0},
        1: {"x": [161 ,161 ,161 , 161],"y": [  89,  89, 149, 149],"z": [10,0,0,10],"name": "right-front" ,"id": 1},
        2: {"x": [-161,-161,-161,-161],"y": [ 149, 149,  89,  89],"z": [10,0,0,10],"name": "left-front"  ,"id": 2},
        3: {"x": [-195,-195,-195,-195],"y": [  30,  30, -30, -30],"z": [10,0,0,10],"name": "left-middle" ,"id": 3},
        4: {"x": [-161,-161,-161,-161],"y": [ -88,-88 ,-148,-148],"z": [10,0,0,10],"name": "left-back"   ,"id": 4},
        5: {"x": [161 ,161 ,161 , 161],"y": [-149,-149, -89, -89],"z": [10,0,0,10],"name": "right-back"  ,"id": 5}
        }
    
    dic_tmplt = \
        {
        0: {"x": 1,"y": 2,"z": 3 ,"name": "right-middle" ,"id": 0},
        1: {"x": 1,"y": 2,"z": 3 ,"name": "right-front"  ,"id": 1},
        2: {"x": 1,"y": 2,"z": 3 ,"name": "left-front"   ,"id": 2},
        3: {"x": 1,"y": 2,"z": 3 ,"name": "left-middle"  ,"id": 3},
        4: {"x": 1,"y": 2,"z": 3 ,"name": "left-back"    ,"id": 4},
        5: {"x": 1,"y": 2,"z": 3 ,"name": "right-back"   ,"id": 5}
        }
    ct1 = BotCartType("ct1",dic_tmplt)
    cj1 = CarSqsType(name="cj1",ctraj_dic = ctraj_tmplt)
    #cj1 = CarSqsType(name="cj1")

    cj1+=ct1
    print(cj1)
    
def dq_test_matmul():
    ctraj_tmplt = \
        {
        0: {"x": [ 95 ,195 ,195 , 195],"y": [ -30, -30,  30,  30],"z": [10,0,0,10],"name": "right-middle","id": 0},
        1: {"x": [ 61 ,161 ,161 , 161],"y": [  89,  89, 149, 149],"z": [10,0,0,10],"name": "right-front" ,"id": 1},
        2: {"x": [-161,-161,-161,-161],"y": [ 149, 149,  89,  89],"z": [10,0,0,10],"name": "left-front"  ,"id": 2},
        3: {"x": [-195,-195,-195,-195],"y": [  30,  30, -30, -30],"z": [10,0,0,10],"name": "left-middle" ,"id": 3},
        4: {"x": [-161,-161,-161,-161],"y": [ -88,-88 ,-148,-148],"z": [10,0,0,10],"name": "left-back"   ,"id": 4},
        5: {"x": [161 ,161 ,161 , 161],"y": [-149,-149, -89, -89],"z": [10,0,0,10],"name": "right-back"  ,"id": 5}
        }
        
    cj1 = CarSqsType(name="cj1",ctraj_dic = ctraj_tmplt)
    mat_gnd2cob = SE3.Trans(0,0,10)
    cj2 = mat_gnd2cob*cj1
    print(cj2)

def dq_test_matsmul():
    ctraj_tmplt = \
        {
        0: {"x": [ 95 ,195 ,195 , 195],"y": [ -30, -30,  30,  30],"z": [10,0,0,10],"name": "right-middle","id": 0},
        1: {"x": [ 61 ,161 ,161 , 161],"y": [  89,  89, 149, 149],"z": [10,0,0,10],"name": "right-front" ,"id": 1},
        2: {"x": [-161,-161,-161,-161],"y": [ 149, 149,  89,  89],"z": [10,0,0,10],"name": "left-front"  ,"id": 2},
        3: {"x": [-195,-195,-195,-195],"y": [  30,  30, -30, -30],"z": [10,0,0,10],"name": "left-middle" ,"id": 3},
        4: {"x": [-161,-161,-161,-161],"y": [ -88,-88 ,-148,-148],"z": [10,0,0,10],"name": "left-back"   ,"id": 4},
        5: {"x": [161 ,161 ,161 , 161],"y": [-149,-149, -89, -89],"z": [10,0,0,10],"name": "right-back"  ,"id": 5}
        }
        
    cj1 = CarSqsType(name="cj1",ctraj_dic = ctraj_tmplt)
    mats_cob2base = HexgnTranType("mats_bdy",3,4,5)
    
    cj2 = mats_cob2base*cj1
    
    print(cj2)

    cj1 = CarSqsType(name="cj2")
    print("cj1",cj1)

def test_apnd():
    # Test appending ctype
    bc = BotCartType()
    ct1 = CarSqsType(name="gait_pose_cseqs")
    ct0 = CarSqsType()
    ct1 = ct1+bc
    ct1 = ct1+bc
    ct1 = ct1+bc

    print(ct1)

    for cpos_fram in ct1:
        print(cpos_fram)
    
    print(ct1 == ct1)
    print(ct1 == ct0)

    bc1 = BotCartType()
    bc1.set_by_idx(0,0,1.2)
    print(ct1.cpos_is_in(bc))
    print(ct1.cpos_is_in(bc1))

def test_redunt_pos():

    cart_tmplt = {
            0: {"x": 0,"y": 0,"z": 10,"name": "right-middle","id": 0},
            1: {"x": 0,"y": 0,"z": 10,"name": "right-front" ,"id": 1},
            2: {"x": 0,"y": 0,"z": 10,"name": "left-front"  ,"id": 2},
            3: {"x": 0,"y": 0,"z": 10,"name": "left-middle" ,"id": 3},
            4: {"x": 0,"y": 0,"z": 10,"name": "left-back"   ,"id": 4},
            5: {"x": 0,"y": 0,"z": 10,"name": "right-back"  ,"id": 5}}
    bc1 = BotCartType(name="ct1",cart_dic = cart_tmplt)

    bc  = BotCartType()
    ct1 = CarSqsType(name="gait_pose_cseqs")
    ct1 = ct1+bc
    ct1 = ct1+bc
    ct1 = ct1+bc
    ct1 = ct1+bc1

    
    print("ct1.get_redunt_mov_idx()",ct1.get_redunt_mov_ids())

if __name__ == "__main__":
    
    # dq_test_CarTraj()
    # dq_test_load_json()
    # dq_test_add_override()
    # dq_test_matmul()
    # dq_test_matsmul()
    #test_apnd()

    test_redunt_pos()
