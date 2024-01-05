from copy import deepcopy
import sys 
sys.path.append("../")
from    typing                     import Union,List
from    collections                import deque
from    custom_type.bot_base_type  import BotBaseType

class ValvPumpActType(BotBaseType):
    __slots__ = ("vpump_onoff","name","NUM_LEGS","action_perid","_iter_idx_")
    TURN_ON,TURN_OFF,NO_ACT  = 1,0,2

    def __init__(self, vpump_onoff=None, name=""):

        self.NUM_LEGS = super().LEG_SZ
        vp_onff_tmplt = {
                0: {"onoff_vpump": self.TURN_OFF,"id": 0,"name": "right-middle"},     
                1: {"onoff_vpump": self.TURN_OFF,"id": 1,"name": "right-front" },
                2: {"onoff_vpump": self.TURN_OFF,"id": 2,"name": "left-front"  },
                3: {"onoff_vpump": self.TURN_OFF,"id": 3,"name": "left-middle" },
                4: {"onoff_vpump": self.TURN_OFF,"id": 4,"name": "left-back"   },    
                5: {"onoff_vpump": self.TURN_OFF,"id": 5,"name": "right-back"  }}     
        
        self.action_perid = 0
        if vpump_onoff == None:
            self.vpump_onoff = vp_onff_tmplt
        else: 
            self.vpump_onoff = deepcopy(vpump_onoff)

        self.name = name

    def form_str(self):
        # Format row coord value
        len_legs = self.NUM_LEGS
        sr_val_ar = [""]*len_legs
        # Loop over each row
        for j in range(len_legs):
            name = "onoff_vpump: "

            x = self.vpump_onoff[j]["onoff_vpump"]
            x_str = str(x)
            sr_val_ar[j] = name + x_str

        # Format names    
        sr_nam_ar = [""]*len_legs
        for j in range(len_legs): # Fixe namne length

            sr_nam_ar[j] = self.vpump_onoff[j]["name"]
            if(len(sr_nam_ar[j])<13):
                sr_nam_ar[j] = sr_nam_ar[j] +" "*(13-len(sr_nam_ar[j]))
            sr_nam_ar[j] = sr_nam_ar[j] + sr_val_ar[j] +"\n"

        # Append each row
        full_str = ""
        for j in range(len_legs):
            full_str = full_str + sr_nam_ar[j]
        full_str = "\n"+full_str

        full_str = self.name+"\n"+full_str+"Action period: "+str(self.action_perid)
        return full_str

    def any_leg_is_off(self)->List[Union[bool,int]]:
        """
        If any leg is off, Return: [True,leg_index]
        If all leg is on, Return: [False,None]
        """

        for idx,one_leg in enumerate(self):
            if one_leg == self.TURN_OFF:
                return True,idx
        return False,None
            
    def any_leg_is_on(self)->List[Union[bool,int]]:
        """
        If any leg is on, Return: [True,leg_index]
        If all leg is off, Return: [False,None]
        """
        for idx,one_leg in enumerate(self):
            if one_leg == self.TURN_ON:
                return True,idx   
        
        return False,None

    def get_legs_on(self)->List[Union[bool,List[int]]]:
        """
        If any leg is on , Return: [True,[leg_index-1,...leg_index-n]]
        If all leg is off, Return: [False,[]]
        """
        is_on = False
        lex_idx = []
        for idx,one_leg in enumerate(self):
            if one_leg == self.TURN_ON:
                is_on = True
                lex_idx = lex_idx +[idx]
        
        return [is_on,lex_idx]
                  
    def get_act_perid(self)->float:
        
        return self.action_perid
    
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

        full_str = self.form_str()
        sys.stdout.write(full_str)
        sys.stdout.flush()  

    def get_num_legs(self):
        return self.NUM_LEGS
    
    def get_onoff_dic(self):
        return self.vpump_onoff
      
    def get_by_idx(self,leg_idx:int)->int:
        """
        Given leg's index number,return valve-pump's actions 
        return  TURN_ON  = 1
                TURN_OFF = 0
                NO_ACT   = 2
        """
        return self.vpump_onoff[leg_idx]["onoff_vpump"]
    
    def get_vpump_dict(self):
        return self.vpump_onoff

    def set_act_perid(self,action_perid:float=0):
            self.action_perid = action_perid
        
    def set_all_legs(self,onoff=True):
        """
        param onoff:    options: 
                        TURN_ON  = 1
                        TURN_OFF = 0
                        NO_ACT   = 2
        """
        for leg_idx in range(self.NUM_LEGS):
            self.set_by_idx(leg_idx,onoff)

    def set_by_idx(self,leg_idx:int,action:int):
        """
        param action:   options: 
                        TURN_ON  = 1
                        TURN_OFF = 0
                        NO_ACT   = 2
        """
        self.vpump_onoff[leg_idx]["onoff_vpump"] = action

    def __iter__(self):
        self._iter_idx_ = 0
        return self    
    
    def __next__(self)->float:
        if self._iter_idx_ < self.get_num_legs():
            one_leg = self.get_by_idx(self._iter_idx_)
            self._iter_idx_ +=1
            return one_leg
        else:
            raise StopIteration

    def __str__(self):
        full_str = self.form_str()
        return full_str

    def __getitem__(self, leg_idx:int)->int:
        """
        Given leg's index number,return valve-pump's actions 
        return  TURN_ON  = 1
                TURN_OFF = 0
                NO_ACT   = 2
        """
        return self.get_by_idx(leg_idx)
      

class ValvPumpSqsType(BotBaseType):
    __slots__ = ("vpump_sqs_dq","name","leg_len","_iter_idx_")
    TURN_ON  = ValvPumpActType.TURN_ON
    TURN_OFF = ValvPumpActType.TURN_OFF
    NO_ACT   = ValvPumpActType.NO_ACT
    
    def __init__(self, name="",vpump_sqs_dic=None ):

        self.vpump_sqs_dq = deque()
        if vpump_sqs_dic == None:
            self.conv_dq2dic()
        else: 
            self.conv_apnd_dic2dq(vpump_sqs_dic)

        self.name = name
        self.leg_len  = super().LEG_SZ
        
    def conv_apnd_dic2dq(self,vpump_sqs_dic:dict=None):
        """
        Convert dictionary type and append to dequeue type trajectory
        vpump_sqs_di = {
                0: {"onoff_vpump": [],"id": 0,"name": "right-middle"},     
                1: {"onoff_vpump": [],"id": 1,"name": "right-front" },
                2: {"onoff_vpump": [],"id": 2,"name": "left-front"  },
                3: {"onoff_vpump": [],"id": 3,"name": "left-middle" },
                4: {"onoff_vpump": [],"id": 4,"name": "left-back"   },    
                5: {"onoff_vpump": [],"id": 5,"name": "right-back"  }}     
        """

        for j in range(len(vpump_sqs_dic[0]["onoff_vpump"])):
            vp = ValvPumpActType(name='vpsq'+str(j))
            for i in range(vp.get_num_legs()):
                act = vpump_sqs_dic[i]["onoff_vpump" ][j]
                vp.set_by_idx(i,act)
            self.vpump_sqs_dq.append(vp)

    def conv_dq2dic(self)->dict:
        """
        Convert self.ctraj_dq (dequeue type) trajectory to dictionary list type, and return
        
        return type: 
        vpump_sqs_dic = \
                0: {"onoff_vpump": [],"id": 0,"name": "right-middle"},     
                1: {"onoff_vpump": [],"id": 1,"name": "right-front" },
                2: {"onoff_vpump": [],"id": 2,"name": "left-front"  },
                3: {"onoff_vpump": [],"id": 3,"name": "left-middle" },
                4: {"onoff_vpump": [],"id": 4,"name": "left-back"   },    
                5: {"onoff_vpump": [],"id": 5,"name": "right-back"  }}   
        """

        len_sqs = len(self.vpump_sqs_dq)
        vpump_sqs_dic = {\
                0: {"onoff_vpump": [0]*len_sqs,"id": 0,"name": "right-middle"},     
                1: {"onoff_vpump": [0]*len_sqs,"id": 1,"name": "right-front" },
                2: {"onoff_vpump": [0]*len_sqs,"id": 2,"name": "left-front"  },
                3: {"onoff_vpump": [0]*len_sqs,"id": 3,"name": "left-middle" },
                4: {"onoff_vpump": [0]*len_sqs,"id": 4,"name": "left-back"   },    
                5: {"onoff_vpump": [0]*len_sqs,"id": 5,"name": "right-back"  }}   
        
        for j in range(len(self.vpump_sqs_dq)):
            bj = self.vpump_sqs_dq[j] # loop over ValvPumpActType() dequeue data
            for i in range(bj.get_num_legs()):
                vpump_sqs_dic[i]["onoff_vpump" ][j] = bj[i]
        return vpump_sqs_dic
    
    def assign_act_perid(self,act_prid_ms:float=0):
        """
        Suction cup needs some time to deplete air, so we need to 
        give it some time to do the job. 
        Only need the time when vpump goes from turn-off to turn-on  
        """
        for isqs,one_vp in enumerate(self):

            # If any pump is from off to on, then add delay period
            [ison,ilegs]=one_vp.get_legs_on() 
            if ison == True:
                for ileg in ilegs:
                    if self[isqs-1][ileg] == one_vp.TURN_OFF:
                        self[isqs].set_act_perid(act_prid_ms)

        
    def clear_dq(self):
        """
        Clear dequeue
        """
        self.vpump_sqs_dq.clear()

    def form_str(self):
        # Format row coord value
        len_legs  = self.get_leg_len()
        sr_val_ar = [""]*len_legs
        leg_arr   = self.get_sqs_len()
        
        vpump_sqs_dic = self.conv_dq2dic()
        # Loop over each row
        for j in range(len_legs):
            name = "onoff_vpump: "
            act_str = ""
            for i in range(leg_arr):
                act = vpump_sqs_dic[j]["onoff_vpump"][i]

                act_str = act_str + str(act) + ", "

            sr_val_ar[j] = name + act_str[0:-2]

        # Format names    
        sr_nam_ar = [""]*len_legs
        for j in range(len_legs): # Fixe namne length

            sr_nam_ar[j] = vpump_sqs_dic[j]["name"]
            if(len(sr_nam_ar[j])<13):
                sr_nam_ar[j] = sr_nam_ar[j] +" "*(13-len(sr_nam_ar[j]))
            sr_nam_ar[j] = sr_nam_ar[j] + sr_val_ar[j] +"\n"

        # Append each row
        full_str = ""
        for j in range(len_legs):
            full_str = full_str + sr_nam_ar[j]
        full_str = "\n"+full_str
        full_str = self.name+"\n"+full_str
        return full_str
    
    def key_str2int(self,str_key_dic:dict)->dict:
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

    def appnd_act_type(self,one_act:ValvPumpActType):
        """
        Given ValvPumpActType, append to tail
        """
        self.vpump_sqs_dq.append(deepcopy(one_act))

    def appnd_valpump_sqs(self,vp_sqs):
        """
        Given ValvPumpSqsType, append to tail
        """
        while vp_sqs.get_sqs_len() !=0:
            self.vpump_sqs_dq.append(vp_sqs.pop_fnt_fram())
        
    def pop_fnt_fram(self)->ValvPumpActType:
        """
        Pop out one frame from front (Pop left).  
        Return None if length == 0
        """
        if self.get_sqs_len() == 0:
            return None 
        
        fst_fram = deepcopy(self.vpump_sqs_dq.popleft())
        return fst_fram
    

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

        full_str = self.form_str()
        sys.stdout.write(full_str)
        sys.stdout.flush()      

    def get_one_act_fram(self,sqs_idx:int)->ValvPumpActType:
        """
        Given sequence index, return actions for each leg.
        Return in type of ValvPumpActType
        """
        one_seq_act = deepcopy(self.vpump_sqs_dq[sqs_idx])
        return one_seq_act

    def get_sqs_len(self)->int:
        return len(self.vpump_sqs_dq)
    
    def get_leg_len(self)->int:
        return self.leg_len
    
    def get_by_idx(self,leg_idx,vpump_idx)->int:
        """
        Givne sequence index and leg index return action status
        return  TURN_ON  = 1
                TURN_OFF = 0
                NO_ACT   = 2
        """
        act_fram = self.get_one_act_fram(vpump_idx)
        return deepcopy(act_fram.get_by_idx(leg_idx))
    
    def get_vpump_dict(self)->dict:
        return self.conv_dq2dic()
    

    def set_by_idx(self,leg_idx,vpump_idx,action):
        """
        Given leg and sequence idx, set action
        action: 
            TURN_ON  = 1
            TURN_OFF = 0
            NO_ACT   = 2
        """
        self.vpump_sqs_dq[vpump_idx].set_by_idx(leg_idx,action)
        
    def set_dq(self,vpump_sqs_dq):
        self.vpump_sqs_dq = vpump_sqs_dq
        
    def set_by_strkey(self,str_key_dic):
        '''
        Json file does not support int key, Convert to int key
        Note: Old deque buffer will be cleared
        '''
        vpump_sqs_dic = self.key_str2int(str_key_dic)
        self.clear_dq()
        self.conv_apnd_dic2dq(vpump_sqs_dic)

    def __iter__(self):
        self._iter_idx_ = 0
        return self    
    
    def __next__(self)->ValvPumpActType:
        if self._iter_idx_ < self.get_sqs_len():
            one_vp = self.vpump_sqs_dq[self._iter_idx_]
            self._iter_idx_ +=1
            return one_vp
        else:
            raise StopIteration
        
    def __add__(self,e):
        """
        Reload the add("+") sign, as append operation
        """
        d = deepcopy(e)
        if isinstance(d,ValvPumpActType):
            vp_dq = deepcopy(self.vpump_sqs_dq)
            vp_dq.append(d)
            apnd_vp_dq = ValvPumpSqsType("Append vpump act sqs")
            apnd_vp_dq.set_dq(vp_dq)
            return apnd_vp_dq
        
        elif isinstance(d,ValvPumpSqsType): 
            vp_dq = deepcopy(self.vpump_sqs_dq)
            for j in range(len(d)):
                vp_dq.append(d[j])
            apnd_vp_dq = ValvPumpSqsType("Append vpump act sqs")
            apnd_vp_dq.set_dq(vp_dq)
            return apnd_vp_dq
        else:
            return NotImplemented

    def __getitem__(self, sqs_idx:int)->ValvPumpActType:
        one_seq_act = self.vpump_sqs_dq[sqs_idx]
        return one_seq_act
            
    def __len__(self)->int:
        return self.get_sqs_len()

    def __str__(self):
        full_str = self.form_str()
        return full_str

def test1():
    import time
    vp0 = ValvPumpActType()
    vp0.set_all_legs(0)
    vp1 = ValvPumpActType()
    vp1.set_all_legs(1)
    vp2 = ValvPumpActType()
    vp2.set_all_legs(2)
    
    vp_sqs = ValvPumpSqsType("vp_sqs\n")
    print(vp_sqs)

    # test append act 
    vp_sqs = vp_sqs+vp0
    vp_sqs = vp_sqs+vp1
    vp_sqs = vp_sqs+vp2
    print(vp_sqs)
    
    # test append sqs
    vp_sqs = vp_sqs+vp_sqs
    print( vp_sqs)
    
def testappend():
    vpump_traj_tmplt = ValvPumpSqsType(name="vpump_traj_tmplt") 
    vp_act = ValvPumpActType(name="vp_act")
    vp_act.set_all_legs(vp_act.TURN_OFF)
    print("*************vp_act: ",vp_act)
    vpump_traj_tmplt.appnd_act_type(vp_act)
    vp_act.set_all_legs(vp_act.TURN_ON)
    vpump_traj_tmplt.appnd_act_type(vp_act)
    
    print("vpump_traj_tmplt: ",vpump_traj_tmplt)

def test_assign_prid():
    vpump_traj = ValvPumpSqsType(name="vpump_traj") 
    vp_act     = ValvPumpActType(name="vp_act"    )
    vp_act.set_all_legs(vp_act.TURN_OFF)
    vpump_traj.appnd_act_type(vp_act)

    vp_act.set_all_legs(vp_act.TURN_ON)
    vpump_traj.appnd_act_type(vp_act)

    for one_vp in vpump_traj:
        #for one_leg in one_vp:
        #    print(one_leg)
        print(one_vp.any_leg_is_off())
        print(one_vp.any_leg_is_on())

    vpump_traj.assign_act_perid(10)

    for one_vp in vpump_traj:
        print(one_vp)


if __name__ == "__main__":
    test_assign_prid()
    