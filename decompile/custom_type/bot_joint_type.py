from copy import deepcopy
import sys 
sys.path.append("../")
from    custom_type.bot_base_type  import BotBaseType
from    typing          import List,Union

class BotJointType(BotBaseType):

    __slots__ = ("jt_dic","name"   ,"jt_nam_arr",
                 "leg_sz","jont_sz","action_perid")

    def __init__(self, name="",joint_dic=None ):
        if joint_dic is not None: 
            if (isinstance(joint_dic,dict) == False or isinstance(name,str)== False):
                raise NameError('fatal error: Incorrect arguments type')

        jtdic_tmplt = {
                0: {"coxa": 0, "femur": 0, "tibia": 0, "name": "right-middle", "id": 0},
                1: {"coxa": 0, "femur": 0, "tibia": 0, "name": "right-front" , "id": 1},
                2: {"coxa": 0, "femur": 0, "tibia": 0, "name": "left-front"  , "id": 2},
                3: {"coxa": 0, "femur": 0, "tibia": 0, "name": "left-middle" , "id": 3},
                4: {"coxa": 0, "femur": 0, "tibia": 0, "name": "left-back"   , "id": 4},
                5: {"coxa": 0, "femur": 0, "tibia": 0, "name": "right-back"  , "id": 5}} 
        
        self.leg_sz     = super().LEG_SZ
        self.jont_sz    = super().JOINT_SZ
        self.jt_nam_arr = super().NAMES_JOINT
        self.action_perid = 0

        if joint_dic == None:
            self.jt_dic = jtdic_tmplt
        else: 
            
            if(isinstance(list(joint_dic.keys())[0],str)):
                self.set_by_strkey(joint_dic)
            else:
                self.jt_dic = deepcopy(joint_dic)
        self.name = name

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

    def form_str(self):
        # Format row coord value
        len_legs = len(self.jt_dic)
        sr_val_ar = [""]*len_legs

        # Loop over each row
        for j in range(len_legs):
            c_str = "coxa: ["
            f_str = " femur: ["
            t_str = " tibia: ["
            c = self.jt_dic[j]["coxa"]
            f = self.jt_dic[j]["femur"]
            t = self.jt_dic[j]["tibia"]

            c_str = c_str + f"{c:+8.2f},"
            f_str = f_str + f"{f:+8.2f},"
            t_str = t_str + f"{t:+8.2f},"

            sr_val_ar[j] = c_str+"]"+f_str+"]"+t_str[0:-1]+"]"

        # Format names    
        sr_nam_ar = [""]*len_legs
        for j in range(len_legs): # Fixe namne length

            sr_nam_ar[j] = self.jt_dic[j]["name"]
            if(len(sr_nam_ar[j])<13):
                sr_nam_ar[j] = sr_nam_ar[j] +" "*(13-len(sr_nam_ar[j]))
            sr_nam_ar[j] = sr_nam_ar[j] + sr_val_ar[j] +"\n"

        # Append each row
        full_str = ""
        for j in range(len_legs):
            full_str = full_str + sr_nam_ar[j]
        full_str = self.name+"\n"+full_str+"Action perid: "+str(self.get_act_perid())

        return full_str
    
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

    def get_act_perid(self)->float:
        return self.action_perid

    def get_jt_dic(self):
        return self.jt_dic
    
    def get_num_legs(self):
        return self.leg_sz
    
    def get_num_joints(self):
        '''
        Joint size for one leg
        '''
        return self.jont_sz
    
    def get_jont_name(self,jt_idx):
        return self.jt_nam_arr[jt_idx]
    
    def get_leg_name(self,leg_idx):
        return self.jt_dic[leg_idx]["name"]
    
    def get_val_by_idx(self,leg_idx,joint_idx):
        '''
        Given leg index and joint index, return value
        joint_idx: range 0-2
        leg_idx : range 0-5
        '''
        jt_nam = self.jt_nam_arr[joint_idx]
        return self.jt_dic[leg_idx][jt_nam]


    def get_arr_by_ileg(self,leg_idx)->List[Union[float,float,float]]:
        '''
        Given leg index and return all joints' val as arr
        leg_idx : range 0-5
        return leg_arr: [coxa_val,femur_val,tibia_val]
        '''
        leg_arr = [0]*self.jont_sz

        for joint_idx in range(self.jont_sz):
            jt_nam = self.jt_nam_arr[joint_idx]
            leg_arr[joint_idx] = self.jt_dic[leg_idx][jt_nam]

        return leg_arr

    def get_jt_dict(self):
        return self.jt_dic
    
    def set_act_perid(self,action_perid:float=0):
        self.action_perid = action_perid

    def set_arr_by_ileg(self,leg_idx:int=0,leg_arr:list=[0,0,0]):
        '''
        Given leg index and return all joints' val as arr
        leg_idx : range 0-5
        leg_arr : [coxa_val,femur_val,tibia_val]
        '''

        for joint_idx in range(self.jont_sz):
            jt_nam = self.jt_nam_arr[joint_idx]
            self.jt_dic[leg_idx][jt_nam] = leg_arr[joint_idx] 

        return leg_arr


    def set_by_idx(self,leg_idx,joint_idx,joint_val):
        jt_nam = self.jt_nam_arr[joint_idx]
        self.jt_dic[leg_idx][jt_nam] = joint_val

    def set_by_jt_nam(self,leg_idx,joint_nam,joint_val):
        self.jt_dic[leg_idx][joint_nam] = joint_val

    def set_all_jt(self,jt_val:float):
        """
        Set all joint to a single value
        """
        for i in range(self.get_num_legs()):
            self.set_arr_by_ileg(i,[jt_val,jt_val,jt_val])
    
    def set_by_strkey(self,json_str):
        '''
        Json file does not support int key, Convert to int key
        
        '''
        self.jt_dic = self.key_str2int(json_str)    


    def __getitem__(self,idx:int)->List[Union[float,float,float]]:
        """
        Given leg's idx, return [x,y,z]
        """
        if isinstance(idx,int):
            pt_arr = self.get_arr_by_ileg(idx)
            return pt_arr 
        else: 
            print("NotImplemented")
            return NotImplemented

    def __eq__(self,obj):
        """
        type obj: BotJointType
        """

        if isinstance(obj,BotJointType) == False: 
            return False
        
        obj_dic=obj.get_jt_dic()
        for key in self.jt_dic.keys():
            if self.jt_dic[key][self.jt_nam_arr[0]] != obj_dic[key][self.jt_nam_arr[0]] or \
               self.jt_dic[key][self.jt_nam_arr[1]] != obj_dic[key][self.jt_nam_arr[1]] or \
               self.jt_dic[key][self.jt_nam_arr[2]] != obj_dic[key][self.jt_nam_arr[2]]:
                return False
        return True

    def __str__(self):
        return self.form_str()

def test_load_json():
    
    jtdic_tmplt = \
        {
        "0": {"coxa": 1971,"femur": 2017,"tibia": 2092 ,"name": "right-middle" ,"id": 0},
        "1": {"coxa": 2600,"femur": 2070,"tibia": 1941 ,"name": "right-front"  ,"id": 1},
        "2": {"coxa": 1396,"femur": 2045,"tibia": 2111 ,"name": "left-front"   ,"id": 2},
        "3": {"coxa": 2056,"femur": 2137,"tibia": 2100 ,"name": "left-middle"  ,"id": 3},
        "4": {"coxa": 2571,"femur": 2100,"tibia": 2050 ,"name": "left-back"    ,"id": 4},
        "5": {"coxa": 1542,"femur": 1841,"tibia": 1611 ,"name": "right-back"   ,"id": 5}
        }
    
    ct1 = BotJointType()
    ct1.set_by_strkey(jtdic_tmplt)
    jtdic_tmplt = \
        {
        "0": {"coxa": 1971,"femur": 2017,"tibia": 2092 ,"name": "right-middle" ,"id": 0},
        "1": {"coxa": 2600,"femur": 2070,"tibia": 1941 ,"name": "right-front"  ,"id": 1},
        "2": {"coxa": 1396,"femur": 2045,"tibia": 2111 ,"name": "left-front"   ,"id": 2},
        "3": {"coxa": 2056,"femur": 2137,"tibia": 2100 ,"name": "left-middle"  ,"id": 3},
        "4": {"coxa": 2571,"femur": 2100,"tibia": 2050 ,"name": "left-back"    ,"id": 4},
        "5": {"coxa": 1542,"femur": 1841,"tibia": 1611.0001 ,"name": "right-back"   ,"id": 5}
        }
    ct2 = BotJointType()
    ct2.set_by_strkey(jtdic_tmplt)

    print("check equal: "+str(ct1==ct2) )

if __name__ == "__main__":
    test_load_json()