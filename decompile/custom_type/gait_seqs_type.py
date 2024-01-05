import json 
import copy
import time
import sys
from copy       import deepcopy

class GaitIdxSeqsType:
    __slots__ = ("gait_seqs","name","map_nam2indx","sqs_len")
    def __init__(self, gait_seqs=None, name=None):

        # Row: pose sequence number. Colum: leg number.  
        seqs_tmplt = \
            {
                0 : {"rm": 0,"rf": 0,"lf": 0,"lm": 0,"lb": 0,"rb": 2, "name": "t0  step1" },
                1 : {"rm": 0,"rf": 0,"lf": 0,"lm": 0,"lb": 0,"rb": 3 ,"name": "t1  step1" },
                2 : {"rm": 0,"rf": 0,"lf": 0,"lm": 0,"lb": 0,"rb": 0 ,"name": "t2  step1" },
                3 : {"rm": 0,"rf": 0,"lf": 0,"lm": 0,"lb": 0,"rb": 1 ,"name": "t3  step1" },
                4 : {"rm": 0,"rf": 0,"lf": 0,"lm": 0,"lb": 0,"rb": 1, "name": "t4  step2" },
                5 : {"rm": 0,"rf": 0,"lf": 0,"lm": 0,"lb": 0,"rb": 1 ,"name": "t5  step2" },
                6 : {"rm": 0,"rf": 0,"lf": 0,"lm": 0,"lb": 0,"rb": 1 ,"name": "t6  step2" },
                7 : {"rm": 0,"rf": 0,"lf": 0,"lm": 0,"lb": 0,"rb": 1 ,"name": "t7  step2" },
                8 : {"rm": 0,"rf": 0,"lf": 0,"lm": 0,"lb": 0,"rb": 1, "name": "t8  step3" },
                9 : {"rm": 0,"rf": 0,"lf": 0,"lm": 0,"lb": 0,"rb": 1 ,"name": "t9  step3" },
                10: {"rm": 0,"rf": 0,"lf": 0,"lm": 0,"lb": 0,"rb": 1 ,"name": "t10 step3" },
                11: {"rm": 0,"rf": 0,"lf": 0,"lm": 0,"lb": 0,"rb": 1 ,"name": "t11 step3" }
            }
        # Leg index order is: 0:rm, 1:rf,...counter-clock... 5:rb
        self.map_nam2indx = ["rm","rf","lf","lm","lb","rb"]

        if (gait_seqs == None):
            self.gait_seqs = seqs_tmplt
        else: 
            self.gait_seqs = deepcopy(gait_seqs)
             
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
   

    def get_sqs_len(self):
        return len(self.gait_seqs)
    
    def get_by_nam(self,tim_idx,leg_nam_str):
        return self.gait_seqs[tim_idx][leg_nam_str]
    
    def get_by_idx(self,tim_idx,leg_idx):
        # tim_idx: time step index
        # leg_idx: leg index, range[0,5] 
        leg_nam_str = self.map_nam2indx[leg_idx]
        return self.gait_seqs[tim_idx][leg_nam_str]

    def get_seqs_by_idxs(self,star_tim_idx,end_tim_idx,star_leg_idx,end_leg_idx):
        # return: A 2*2 matrix Row: time unit. Colum: legs index
        seq_mat = []

        if(end_tim_idx>star_tim_idx and end_leg_idx>star_leg_idx):
            for t_idx in range(star_tim_idx,end_tim_idx): # loop each row 
                one_leg_seqs =[]
                for leg_idx in range(star_leg_idx,end_leg_idx):
                    one_leg_seqs = one_leg_seqs+[self.get_one_by_idx(t_idx,leg_idx)]
                seq_mat = seq_mat+[one_leg_seqs]
        return seq_mat
    
    def get_dict(self):
        return self.gait_seqs
    
    def set_by_strkey(self,json_str):
        '''
        Json file does not support int key, Convert to int key

        '''
        self.gait_seqs = self.key_str2int(json_str)

 
    def __str__(self):
        #self.gait_seqs
        rstr=''
        for key in self.gait_seqs:
            rstr = rstr+ str(key) + ": "+str(self.gait_seqs[key]) + "\n"
        return rstr
    
def test_load_json():
    gs1 = GaitIdxSeqsType()
    out_file = open("../config/ctraj_sqs_tright.json", "r") 
    trght_gaits = json.load(out_file)
    gseqs = trght_gaits["GAIT_TRAJ_IDX_SEQS"]

    gs1.set_by_strkey(gseqs)

    gsqs = gs1.get_seqs_by_idxs(0,5,0,6)
    print(gsqs)

if __name__ == "__main__":
    test_load_json()