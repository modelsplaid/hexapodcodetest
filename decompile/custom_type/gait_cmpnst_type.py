import json 
import copy
import time
import sys
from copy       import deepcopy

class GaitCmpnstSeqsType:
    __slots__ = ("cmpnst_seqs","name","map_nam2indx","sqs_len")
    def __init__(self, cmpnst_seqs=None, name=None):

        # Row: pose sequence number. Colum: leg number.  
        cmpnst_tmplt = \
            {
            0 : {"rm": {"x":0,"y":0,"z":0},"rf": {"x":0,"y":0,"z":0},"lf": {"x":0,"y":0,"z":0},"lm": {"x":0,"y":0,"z":0},"lb": {"x":0,"y":0,"z":0},"rb": {"x":0,"y":0,"z":0} ,"name": "t0  step1" },
            1 : {"rm": {"x":0,"y":0,"z":0},"rf": {"x":0,"y":0,"z":0},"lf": {"x":0,"y":0,"z":0},"lm": {"x":0,"y":0,"z":0},"lb": {"x":0,"y":0,"z":0},"rb": {"x":0,"y":0,"z":0} ,"name": "t1  step1" },
            2 : {"rm": {"x":0,"y":0,"z":0},"rf": {"x":0,"y":0,"z":0},"lf": {"x":0,"y":0,"z":0},"lm": {"x":0,"y":0,"z":0},"lb": {"x":0,"y":0,"z":0},"rb": {"x":0,"y":0,"z":0} ,"name": "t2  step1" },
            3 : {"rm": {"x":0,"y":0,"z":0},"rf": {"x":0,"y":0,"z":0},"lf": {"x":0,"y":0,"z":0},"lm": {"x":0,"y":0,"z":0},"lb": {"x":0,"y":0,"z":0},"rb": {"x":0,"y":0,"z":0} ,"name": "t3  step1" },
            4 : {"rm": {"x":0,"y":0,"z":0},"rf": {"x":0,"y":0,"z":0},"lf": {"x":0,"y":0,"z":0},"lm": {"x":0,"y":0,"z":0},"lb": {"x":0,"y":0,"z":0},"rb": {"x":0,"y":0,"z":0} ,"name": "t4  step2" },
            5 : {"rm": {"x":0,"y":0,"z":0},"rf": {"x":0,"y":0,"z":0},"lf": {"x":0,"y":0,"z":0},"lm": {"x":0,"y":0,"z":0},"lb": {"x":0,"y":0,"z":0},"rb": {"x":0,"y":0,"z":0} ,"name": "t5  step2" },
            6 : {"rm": {"x":0,"y":0,"z":0},"rf": {"x":0,"y":0,"z":0},"lf": {"x":0,"y":0,"z":0},"lm": {"x":0,"y":0,"z":0},"lb": {"x":0,"y":0,"z":0},"rb": {"x":0,"y":0,"z":0} ,"name": "t6  step2" },
            7 : {"rm": {"x":0,"y":0,"z":0},"rf": {"x":0,"y":0,"z":0},"lf": {"x":0,"y":0,"z":0},"lm": {"x":0,"y":0,"z":0},"lb": {"x":0,"y":0,"z":0},"rb": {"x":0,"y":0,"z":0} ,"name": "t7  step2" },
            8 : {"rm": {"x":0,"y":0,"z":0},"rf": {"x":0,"y":0,"z":0},"lf": {"x":0,"y":0,"z":0},"lm": {"x":0,"y":0,"z":0},"lb": {"x":0,"y":0,"z":0},"rb": {"x":0,"y":0,"z":0} ,"name": "t8  step3" },
            9 : {"rm": {"x":0,"y":0,"z":0},"rf": {"x":0,"y":0,"z":0},"lf": {"x":0,"y":0,"z":0},"lm": {"x":0,"y":0,"z":0},"lb": {"x":0,"y":0,"z":0},"rb": {"x":0,"y":0,"z":0} ,"name": "t9  step3" },
            10: {"rm": {"x":0,"y":0,"z":0},"rf": {"x":0,"y":0,"z":0},"lf": {"x":0,"y":0,"z":0},"lm": {"x":0,"y":0,"z":0},"lb": {"x":0,"y":0,"z":0},"rb": {"x":0,"y":0,"z":0} ,"name": "t10 step3" },
            11: {"rm": {"x":0,"y":0,"z":0},"rf": {"x":0,"y":0,"z":0},"lf": {"x":0,"y":0,"z":0},"lm": {"x":0,"y":0,"z":0},"lb": {"x":0,"y":0,"z":0},"rb": {"x":0,"y":0,"z":0} ,"name": "t11 step3" }
            }
        # Leg index order is: 0:rm, 1:rf,...counter-clock... 5:rb
        self.map_nam2indx = ["rm","rf","lf","lm","lb","rb"]

        if (cmpnst_seqs == None):
            self.cmpnst_seqs = cmpnst_tmplt
        else: 
            self.cmpnst_seqs = deepcopy(cmpnst_seqs)
             
        self.name  = name

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
    

    def get_cmpnst_sqs_len(self):
        return len(self.cmpnst_seqs)
    
    def get_cmpnst_by_nam(self,traj_idx,leg_nam_str):

        x = self.cmpnst_seqs[traj_idx][leg_nam_str]["x"]
        y = self.cmpnst_seqs[traj_idx][leg_nam_str]["y"]
        z = self.cmpnst_seqs[traj_idx][leg_nam_str]["z"]

        return [x,y,z]
    
    def get_cmpnst_by_idx(self,leg_idx,traj_idx):
        # traj_idx: time step index
        # leg_idx: leg index, range[0,5] 

        leg_nam_str = self.map_nam2indx[leg_idx]
        x = self.cmpnst_seqs[traj_idx][leg_nam_str]["x"]
        y = self.cmpnst_seqs[traj_idx][leg_nam_str]["y"]
        z = self.cmpnst_seqs[traj_idx][leg_nam_str]["z"]

        return [x,y,z]

    def get_dict(self):
        return self.cmpnst_seqs
    
    def set_by_strkey(self,json_str):
        '''
        Json file does not support int key, Convert to int key

        '''
        self.cmpnst_seqs = self.key_str2int(json_str)


def test_load_json():
    gs1 = GaitCmpnstSeqsType()
    out_file = open("../config/ctraj_sqs_tright.json", "r") 
    trght_gaits = json.load(out_file)
    gseqs = trght_gaits["GAIT_CMPENSAT_SEQS"]

    gs1.set_by_strkey(gseqs)

    print(gs1.cmpnst_seqs)

if __name__ == "__main__":
    test_load_json()