"""
To do linear fitting for each joint. 

Line fit equation: y = a*x + b 

This type is usually used for raw torque to nm torque, or servo pulse to pulse deg conversion

"""

from copy import deepcopy
import sys
sys.path.append("../")

from    custom_type.bot_base_type  import BotBaseType

class BotLinFitType(BotBaseType):
    __slots__ = ("jt_dic","name","leg_sz","jont_sz","jt_nam_arr")

    def __init__(self, name="",joint_dic=None ):
        self.leg_sz     = super().LEG_SZ
        self.jont_sz    = super().JOINT_SZ
        self.jt_nam_arr = super().NAMES_JOINT

        if joint_dic is not None: 
            if (isinstance(joint_dic,dict) == False or isinstance(name,str)== False):
                raise NameError('fatal error: Incorrect arguments type')

        jtdic_tmplt = {
                0: {"coxa": {"b": 0, "c": 0}, "femur": {"b": 0, "c": 0}, "tibia": {"b": 0, "c": 0}, "name": "right-middle", "id": 0},
                1: {"coxa": {"b": 0, "c": 0}, "femur": {"b": 0, "c": 0}, "tibia": {"b": 0, "c": 0}, "name": "right-front" , "id": 1},
                2: {"coxa": {"b": 0, "c": 0}, "femur": {"b": 0, "c": 0}, "tibia": {"b": 0, "c": 0}, "name": "left-front"  , "id": 2},
                3: {"coxa": {"b": 0, "c": 0}, "femur": {"b": 0, "c": 0}, "tibia": {"b": 0, "c": 0}, "name": "left-middle" , "id": 3},
                4: {"coxa": {"b": 0, "c": 0}, "femur": {"b": 0, "c": 0}, "tibia": {"b": 0, "c": 0}, "name": "left-back"   , "id": 4},
                5: {"coxa": {"b": 0, "c": 0}, "femur": {"b": 0, "c": 0}, "tibia": {"b": 0, "c": 0}, "name": "right-back"  , "id": 5}
                }         

        if joint_dic == None:
            self.jt_dic = jtdic_tmplt
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

        print("var name: "+str(self.name) )
        # Format row coord value
        len_legs = len(self.jt_dic)
        sr_val_ar = [""]*len_legs

        # Loop over each row
        for j in range(len_legs):
            c_str = "coxa: ["
            f_str = " femur: ["
            t_str = " tibia: ["

            b_c = self.jt_dic[j]["coxa" ]["b"]
            b_f = self.jt_dic[j]["femur"]["b"]
            b_t = self.jt_dic[j]["tibia"]["b"]

            c_c = self.jt_dic[j]["coxa" ]["c"]
            c_f = self.jt_dic[j]["femur"]["c"]
            c_t = self.jt_dic[j]["tibia"]["c"]

            c_str = c_str + "b: " + f"{b_c:+8.2f}, c: "+ f"{c_c:+8.2f}"
            f_str = f_str + "b: " + f"{b_f:+8.2f}, c: "+ f"{c_f:+8.2f}"
            t_str = t_str + "b: " + f"{b_t:+8.2f}, c: "+ f"{c_t:+8.2f}"

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
        full_str = self.name+"\n"+full_str

        return full_str

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
    
    def get_bc_by_idx(self,leg_idx,joint_idx):
        '''
        Given leg index and joint index, return bc value, where y = a*x + b 
        joint_idx: range 0-2
        leg_idx  : range 0-5
        Return   : [b,c] in float
        '''
        jt_nam = self.jt_nam_arr[joint_idx]
        b = self.jt_dic[leg_idx][jt_nam]["b"]
        c = self.jt_dic[leg_idx][jt_nam]["c"]

        return [b,c]

    def get_arr_by_ileg(self,leg_idx):
        '''
        Given leg index and return all joints' val as arr, where y = a*x + b 
        leg_idx : range 0-5
        return leg_arr: [[coxa_b,c],[femur_b,c],[tibia_b.c]]
        '''
        leg_arr = [0]*self.jont_sz
        bc_arr  = [0]*2
        for joint_idx in range(self.jont_sz):
            jt_nam = self.jt_nam_arr[joint_idx]
            bc_arr[0] = self.jt_dic[leg_idx][jt_nam]["b"]
            bc_arr[1] = self.jt_dic[leg_idx][jt_nam]["c"]
            leg_arr[joint_idx] = deepcopy(bc_arr)
        return leg_arr

    def get_jt_dict(self):
        return self.jt_dic
    
    def set_arr_by_ileg(self,leg_idx:int=0,leg_arr:list=[[0,0],[0,0],[0,0]]):
        '''
        Given leg index and return all joints' val as arr, where y = a*x + b 
        leg_idx : range 0-5
        leg_arr : [[coxa_b,c],[femur_b,c],[tibia_b,c]]

        '''
        for joint_idx in range(self.jont_sz):
            
            jt_nam = self.jt_nam_arr[joint_idx]

            self.jt_dic[leg_idx][jt_nam]["b"] = leg_arr[joint_idx][0]
            self.jt_dic[leg_idx][jt_nam]["c"] = leg_arr[joint_idx][1]


    def set_bc_by_idx(self,leg_idx,joint_idx,bc_arr = [0,0]):
        """
        Given bc array, set to specified leg's joint , where y = a*x + b 
        Param leg_idx   : 0--5
        Param joint_idx : 0--2
        Param bc_arr    : 2d array
        
        """

        jt_nam = self.jt_nam_arr[joint_idx]
        self.jt_dic[leg_idx][jt_nam]["b"] = bc_arr[0]
        self.jt_dic[leg_idx][jt_nam]["c"] = bc_arr[1]

    def set_bc_by_jt_nam(self,leg_idx,joint_nam,bc_arr = [0,0]):
        """
        Given bc array, set to specified leg's joint , where y = a*x + b 
        
        """

        self.jt_dic[leg_idx][joint_nam]["b"] = bc_arr[0]
        self.jt_dic[leg_idx][joint_nam]["c"] = bc_arr[1]



    def set_by_strkey(self,json_str):
        '''
        Json file does not support int key, Convert to int key
        
        '''
        self.jt_dic = self.key_str2int(json_str)   


    def __str__(self):
        return self.form_str()
    
 
def test_load_json():
    
    jtdic_tmplt = {
            "0": {"coxa": {"b": 0, "c": 0}, "femur": {"b": 0, "c": 0}, "tibia": {"b": 0, "c": 0}, "name": "right-middle", "id": 0},
            "1": {"coxa": {"b": 0, "c": 0}, "femur": {"b": 0, "c": 0}, "tibia": {"b": 0, "c": 0}, "name": "right-front" , "id": 1},
            "2": {"coxa": {"b": 0, "c": 0}, "femur": {"b": 0, "c": 0}, "tibia": {"b": 0, "c": 0}, "name": "left-front"  , "id": 2},
            "3": {"coxa": {"b": 0, "c": 0}, "femur": {"b": 0, "c": 0}, "tibia": {"b": 0, "c": 0}, "name": "left-middle" , "id": 3},
            "4": {"coxa": {"b": 0, "c": 0}, "femur": {"b": 0, "c": 0}, "tibia": {"b": 0, "c": 0}, "name": "left-back"   , "id": 4},
            "5": {"coxa": {"b": 0, "c": 0}, "femur": {"b": 0, "c": 0}, "tibia": {"b": 0, "c": 0}, "name": "right-back"  , "id": 5}
            } 
    
    ct2 = BotLinFitType()
    ct2.set_by_strkey(jtdic_tmplt)

    print("ct1: "+str(ct2) )

    ct2.set_arr_by_ileg(4,[[1,2],[3,4],[5,6]])

    
    print("get_arr_by_ileg: "+ str(ct2.get_arr_by_ileg(4)))

    ct2.set_bc_by_idx(1,2,[2,7])

    print("get: "+str(ct2.get_bc_by_idx(1,2)) )
    ct2.print_table()

if __name__ == "__main__":
    test_load_json()