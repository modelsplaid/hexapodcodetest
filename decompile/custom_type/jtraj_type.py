import sys
sys.path.append("../")

from collections                import deque
from copy                       import deepcopy
from custom_type.bot_joint_type import BotJointType
from custom_type.bot_base_type  import BotBaseType

class JTrajType(BotBaseType):

    __slots__ = ("name","jtraj_dq","leg_sz","_iter_idx_")

    def __init__(self, name="",**kwds):
        """
        Case1: 
              Init by given a dictionary: 
              jt1 = JTrajType(name="jt1",jtraj_dic=traj_dict)
              traj_dict is the type of jtraj_tmplt

        Case2: 
              Init as empty trajectory:
              jt1 = JTrajType(name="jt1")

        Case3: Init by specify initial value and trajectory length
              jt1 = JTrajType(name="jt1",init_val=x,traj_len=y)
        """

        self.leg_sz   = super().LEG_SZ
        self.jtraj_dq = deque()

        #print(list(kwds.keys()))
        # Case 1: Init by given a dictionary:
        if len(kwds.keys())==1 and list(kwds.keys())[0]=="jtraj_dic":
            self.name  = name
            self.conv_apnd_dic2dq(deepcopy(kwds["jtraj_dic"]))
            self.conv_dq2dic()
            return
        
        # Case 2: Init as empty trajectory.
        elif len(kwds.keys())==0:
            self.name  = name
            return
        
        # Case 3=: Init Init by specify initial value and trajectory length.
        elif len(kwds.keys())==2 and isinstance(kwds["traj_len"],int): 
            init_val = kwds["init_val"]
            traj_len = kwds["traj_len"]
            jtraj_tmplt = \
                {
                0: {"coxa": [init_val]*traj_len, "femur": [init_val]*traj_len, "tibia": [init_val]*traj_len, "name": "right-middle", "id": 0},
                1: {"coxa": [init_val]*traj_len, "femur": [init_val]*traj_len, "tibia": [init_val]*traj_len, "name": "right-front" , "id": 1},
                2: {"coxa": [init_val]*traj_len, "femur": [init_val]*traj_len, "tibia": [init_val]*traj_len, "name": "left-front"  , "id": 2},
                3: {"coxa": [init_val]*traj_len, "femur": [init_val]*traj_len, "tibia": [init_val]*traj_len, "name": "left-middle" , "id": 3},
                4: {"coxa": [init_val]*traj_len, "femur": [init_val]*traj_len, "tibia": [init_val]*traj_len, "name": "left-back"   , "id": 4},
                5: {"coxa": [init_val]*traj_len, "femur": [init_val]*traj_len, "tibia": [init_val]*traj_len, "name": "right-back"  , "id": 5}
                }
            
            self.name = name
            self.conv_apnd_dic2dq(jtraj_tmplt)
            self.conv_dq2dic()
            return
        
    def conv_apnd_dic2dq(self,jtraj_dic:dict=None):
        """
        Convert dictionary type and append to dequeue type trajectory
        jtraj_dic = \
        {
        0: {"coxa": [t1...tn],"femur": [t1...tn],"tibia": [t1...tn],"name": "right-middle","id": 0},
        1: {"coxa": [t1...tn],"femur": [t1...tn],"tibia": [t1...tn],"name": "right-front" ,"id": 1},
        2: {"coxa": [t1...tn],"femur": [t1...tn],"tibia": [t1...tn],"name": "left-front"  ,"id": 2},
        3: {"coxa": [t1...tn],"femur": [t1...tn],"tibia": [t1...tn],"name": "left-middle" ,"id": 3},
        4: {"coxa": [t1...tn],"femur": [t1...tn],"tibia": [t1...tn],"name": "left-back"   ,"id": 4},
        5: {"coxa": [t1...tn],"femur": [t1...tn],"tibia": [t1...tn],"name": "right-back"  ,"id": 5}
        }
        """

        for j in range(len(jtraj_dic[0]["coxa"])):
            bj = BotJointType(name='jsq'+str(j))
            for i in range(bj.get_num_legs()):
                c = jtraj_dic[i]["coxa" ][j]
                f = jtraj_dic[i]["femur"][j]
                t = jtraj_dic[i]["tibia"][j]
                bj.set_arr_by_ileg(i,[c,f,t])
            self.jtraj_dq.append(bj)

    def conv_dq2dic(self)->dict:
        """
        Convert self.ctraj_dq (dequeue type) trajectory to dictionary list type, and return
        
        return type: 
        jtraj_dic = \
        {
        0: {"coxa": [t1...tn],"femur": [t1...tn],"tibia": [t1...tn],"name": "right-middle","id": 0},
        1: {"coxa": [t1...tn],"femur": [t1...tn],"tibia": [t1...tn],"name": "right-front" ,"id": 1},
        2: {"coxa": [t1...tn],"femur": [t1...tn],"tibia": [t1...tn],"name": "left-front"  ,"id": 2},
        3: {"coxa": [t1...tn],"femur": [t1...tn],"tibia": [t1...tn],"name": "left-middle" ,"id": 3},
        4: {"coxa": [t1...tn],"femur": [t1...tn],"tibia": [t1...tn],"name": "left-back"   ,"id": 4},
        5: {"coxa": [t1...tn],"femur": [t1...tn],"tibia": [t1...tn],"name": "right-back"  ,"id": 5}
        }
        """

        len_sqs = len(self.jtraj_dq)
        jtraj_dic = \
            {
            0: {"coxa": [0]*len_sqs,"femur": [0]*len_sqs,"tibia": [0]*len_sqs,"name": "right-middle","id": 0},
            1: {"coxa": [0]*len_sqs,"femur": [0]*len_sqs,"tibia": [0]*len_sqs,"name": "right-front" ,"id": 1},
            2: {"coxa": [0]*len_sqs,"femur": [0]*len_sqs,"tibia": [0]*len_sqs,"name": "left-front"  ,"id": 2},
            3: {"coxa": [0]*len_sqs,"femur": [0]*len_sqs,"tibia": [0]*len_sqs,"name": "left-middle" ,"id": 3},
            4: {"coxa": [0]*len_sqs,"femur": [0]*len_sqs,"tibia": [0]*len_sqs,"name": "left-back"   ,"id": 4},
            5: {"coxa": [0]*len_sqs,"femur": [0]*len_sqs,"tibia": [0]*len_sqs,"name": "right-back"  ,"id": 5}
            }   
        
        for j in range(len(self.jtraj_dq)):

            bj = self.jtraj_dq[j] # loop over BotCartType() dequeue data
            for i in range(bj.get_num_legs()):
                [c,f,t] = bj[i]
                jtraj_dic[i]["coxa" ][j] = c
                jtraj_dic[i]["femur"][j] = f
                jtraj_dic[i]["tibia"][j] = t
        return jtraj_dic

    def clear_dq(self):
        """
        Clear dequeue
        """
        self.jtraj_dq.clear()

    def key_str2int(self,str_key_dic):
        '''
        After json.load(out_file), json does not support int type key in dictionary, 
        so I created this function to do that.

        :param str_key_dic : A dictionary which its' key is a str(int) type
        :type  str_key_dic : Dictionary 
        
        :return int_key_dic: A dictionary which its' key is a int type 
        :type   int_key_dic: Dictionary 
        '''

        self.clear_dq()
        int_key_dic = dict()
        for strkey in str_key_dic:
            int_key_dic[int(strkey)] = str_key_dic[strkey]
        return int_key_dic

    
    def print_table(self,keep_old=False):
        """
        Print message in a table form
        Param keep_old: =True : When scroll up terminal, will see old record
                        =False: No record

        Move curser to origin reference: https://github.com/gravmatt/py-term
        """

        hom_pos  = '\033[H'
        clr_str  = '\033[2J'

        if keep_old == True:
            sys.stdout.write(clr_str)

        sys.stdout.write(hom_pos)
        sys.stdout.flush()

        apend_str = self.form_str()
        sys.stdout.write(apend_str)
        sys.stdout.flush()   

    def form_str(self):
        jtraj_dic = self.conv_dq2dic()
        # Format row coord value
        len_arr  = len(jtraj_dic[0]["coxa"])
        len_legs = len(jtraj_dic)
        sr_val_ar = [""]*len_legs

        for j in range(len_legs):
            co_str = "coxa: ["
            fe_str = " femur: ["
            ti_str = " tibia: ["
            for i in range(len_arr):
                c = jtraj_dic[j]["coxa" ][i]
                f = jtraj_dic[j]["femur"][i]
                t = jtraj_dic[j]["tibia"][i]

                co_str = co_str + f"{c:+7.2f},"
                fe_str = fe_str + f"{f:+7.2f},"
                ti_str = ti_str + f"{t:+7.2f},"

            sr_val_ar[j] = co_str+"],"+fe_str+"],"+ti_str[0:-1]+"]"

        # Format names
        sr_nam_ar = [""]*len_legs
        for j in range(len_legs): # Fixe namne length

            sr_nam_ar[j] = jtraj_dic[j]["name"]
            if(len(sr_nam_ar[j])<13):
                sr_nam_ar[j] = sr_nam_ar[j] +" "*(13-len(sr_nam_ar[j]))
            sr_nam_ar[j] = sr_nam_ar[j] + sr_val_ar[j] +"\n"

        # Append each row
        full_str = ""
        for j in range(len_legs):
            full_str = full_str + sr_nam_ar[j]
        full_str = self.name+": \n"+full_str
        
        return full_str

    def pop_fnt_fram(self)->BotJointType:
        """
        Pop out one frame from front. 
        Return None if length == 0
        """

        if self.get_traj_len() == 0: 
            return None 
        
        # Get first fram 
        fst_fram = deepcopy(self.jtraj_dq.popleft())
        return fst_fram
    
    def appnd_jpose(self,jpose:BotJointType):
        """
        Given a jpose type value, append jpose to tail
        """
        self.jtraj_dq.append(deepcopy(jpose))
        
    def appnd_jtraj(self,jtraj):
        while jtraj.get_traj_len() != 0:
            fst_fram = jtraj.pop_fnt_fram()
            self.appnd_jpose(fst_fram)
            
    def set_by_strkey(self,json_str):
        '''
        Json file does not support int key, Convert to int key. 
        Note: old deque value will be cleared
        
        '''
        self.clear_dq()
        jtraj_dic = self.key_str2int(json_str)
        self.conv_apnd_dic2dq(jtraj_dic)
        self.conv_dq2dic()
        
    def set_dq(self,jtraj_dq):
        self.jtraj_dq = jtraj_dq

    def set_one_leg(self,leg_idx,jtraj_idx,*args,**kwds):
        """
        Arguments: 
        case 1: *args is pt=[0,0,0]
        case 2: **kwds choises are:  coxa=num, femur=num,tibia=num
    
        Example1 set a leg: 
            jt1 = JTraj(name="ct1")
            jt1.set_one_leg(0,0,[10,45,90])
            print("arr"+str(ct1.get_one_leg(0,0)))
    
        Example2 set a let by specifying one or more joint: 
            jt1.set_one_leg(1,0,"coxa"=10,"femur"=45,"tibia"=90)
            print("separate"+str(jt1.get_one_leg(1,0)))
            
            ct1.set_one_pt(3,2,coxa=99,tibia=88)
            print("separate"+str(ct1.get_one_pt(3,2)))
        """

        if len(args) == 1 and isinstance(args[0], list):
            self.jtraj_dq[jtraj_idx].\
                set_arr_by_ileg(leg_idx,[args[0][0],args[0][1],args[0][2]])

            return 
        
        if len(args) == 0 and len(kwds.keys()) > 0:
            for axis_name in kwds.keys(): # keys are any from : 'coxa' , 'femur' , 'tibia' 
                self.jtraj_dq[jtraj_idx].\
                    set_by_jt_nam(leg_idx,axis_name,kwds[axis_name])
            return
        
        raise NameError('fatal error: Incorrect arguments')

    def get_leg_len(self):
        return self.leg_sz
    
    def get_traj_len(self):
        return len(self.jtraj_dq)

    def get_jtraj_dic(self):
        jtraj_dic = self.conv_dq2dic()
        return jtraj_dic

    def get_one_jpos_fram(self,jtraj_idx:int)->BotJointType:
        """
        Given a trajectory index, return poses for every leg
        """
        one_jpose = deepcopy(self.jtraj_dq[jtraj_idx])
        return one_jpose
    
    def get_one_leg(self,leg_idx,jtraj_idx):
        '''
        Example: 
            jt1 = JTrajType()
            [c,f,t] = jt1.get_one_leg(4,1)
        '''
        jpose = self.jtraj_dq[jtraj_idx] # Type of BotJointType
        [c,f,t]= deepcopy(jpose.get_arr_by_ileg(leg_idx))

        return [c,f,t]

    def iadd (self,d):
        """
        Append to current trajectory given CarSqsType or BotCartType
        Case1 : 
            t1 = BotJointType("jt1",dic_tmplt)
            j1 = JtrajType(name="j1")
            j1 += t1

        Case2 : 
            j0 = BotJointType(name="j0")
            j1 = BotJointType(name="j1")
            j1 += j1+j0 
        """
        pass 
        self.jtraj_dq = self.__add__(d)

    def __add__(self,e):

        # Reload the add("+") sign, as append operation
        d = deepcopy(e)
        if isinstance(d,BotJointType):
            jtraj_dq = deepcopy(self.jtraj_dq)
            jtraj_dq.append(d)
            apnd_jtraj_dq = JTrajType("Append JTraj")
            apnd_jtraj_dq.set_dq(jtraj_dq)
            return apnd_jtraj_dq
        
        elif isinstance(d,JTrajType): 
            jtraj_dq = deepcopy(self.jtraj_dq)

            for j in range(len(d)):
                jtraj_dq.append(d[j])
            apnd_jtraj_dq = JTrajType("Append JTraj")
            apnd_jtraj_dq.set_dq(jtraj_dq)

            return apnd_jtraj_dq

        else:
            return NotImplemented

    def __iter__(self):
        self._iter_idx_ = 0
        return self    
    
    def __next__(self)->BotJointType:
        if self._iter_idx_ < self.get_traj_len():
            one_jp = self.jtraj_dq[self._iter_idx_]
            self._iter_idx_ += 1
            return one_jp
        else:
            raise StopIteration
        

    def __len__(self):
        """
        Get trajectory length  
        return [trajectory_length]
        """
        return self.get_traj_len()
    
    def __getitem__(self, traj_idx:int)->BotJointType:
        """
        Given a trajectory index, return a frame of jpose 
        """
        return self.get_one_jpos_fram(traj_idx)

    def __str__(self):
        return self.form_str()


def test_load_json():

    dickey= \
        {
        0: {"coxa": [13,14], "femur": [14,150], "tibia": [15,130], "name": "right-middle", "id": 0},
        1: {"coxa": [16,17], "femur": [17,18 ], "tibia": [18,16 ], "name": "right-front" , "id": 1},
        2: {"coxa": [7 ,8 ], "femur": [8 ,9  ], "tibia": [9 ,7  ], "name": "left-front"  , "id": 2},
        3: {"coxa": [4 ,5 ], "femur": [5 ,6  ], "tibia": [6 ,4  ], "name": "left-middle" , "id": 3},
        4: {"coxa": [1 ,2 ], "femur": [2 ,3  ], "tibia": [3 ,1  ], "name": "left-back"   , "id": 4},
        5: {"coxa": [10,11], "femur": [11,12 ], "tibia": [12,10 ], "name": "right-back"  , "id": 5}
        }
        
    jt1 = JTrajType(name="t1",jtraj_dic=dickey)
    print(jt1)

    strkey= \
        {
        "0": {"coxa": [113,14], "femur": [14,2150], "tibia": [15,3130], "name": "right-middle", "id": 0},
        "1": {"coxa": [116,17], "femur": [17,218 ], "tibia": [18,316 ], "name": "right-front" , "id": 1},
        "2": {"coxa": [17 ,8 ], "femur": [8 ,29  ], "tibia": [9 ,37  ], "name": "left-front"  , "id": 2},
        "3": {"coxa": [14 ,5 ], "femur": [5 ,26  ], "tibia": [6 ,34  ], "name": "left-middle" , "id": 3},
        "4": {"coxa": [11 ,2 ], "femur": [2 ,23  ], "tibia": [3 ,31  ], "name": "left-back"   , "id": 4},
        "5": {"coxa": [110,11], "femur": [11,212 ], "tibia": [12,310 ], "name": "right-back"  , "id": 5}
        }
        
    jt1 = JTrajType()
    jt1.set_by_strkey(strkey)
    print(jt1)

    leg_angs = jt1.get_one_leg(2,1)
    print("leg_angs: "+str(leg_angs))

    jt1.set_one_leg(3,0,[100,200,300])
    print(jt1)

    jt1.set_one_leg(4,1,coxa=500,tibia=700)
    print("jt1: \n",jt1)
    cft = jt1.get_one_leg(4,1)
    print(cft)

    jtraj_tmplt = \
            {
            0: {"coxa": [], "femur": [], "tibia": [], "name": "right-middle", "id": 0},
            1: {"coxa": [], "femur": [], "tibia": [], "name": "right-front" , "id": 1},
            2: {"coxa": [], "femur": [], "tibia": [], "name": "left-front"  , "id": 2},
            3: {"coxa": [], "femur": [], "tibia": [], "name": "left-middle" , "id": 3},
            4: {"coxa": [], "femur": [], "tibia": [], "name": "left-back"   , "id": 4},
            5: {"coxa": [], "femur": [], "tibia": [], "name": "right-back"  , "id": 5}
            }
    
    jt2 = JTrajType(jtraj_dic=jtraj_tmplt)
    print("jt2 \n"+str(jt2))

    jt3 = JTrajType(jtraj_dic=jtraj_tmplt)
    print("jt3 \n"+str(jt3))

    print("aaa")
    jt4 = JTrajType(name="ct4",init_val=3,traj_len=5)
    print("jt4: \n "+str(jt4))

    print("jt1+jt1: ",jt1+jt1 )
    print("jt1+jt2: ",jt1+jt2 )
    print("jt2+jt1: ",jt2+jt1 )

    bj = BotJointType()
    print("jt2+bj: ",jt2+bj )
if __name__ == "__main__":
    #test_CarTraj()
    test_load_json()
