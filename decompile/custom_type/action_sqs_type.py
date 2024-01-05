
import sys 
import json
sys.path.append("./")

from    copy                      import deepcopy
from    typing                    import List,Union

from custom_type.walk_dir_type    import WalkDirType
from custom_type.valv_pump_type   import ValvPumpSqsType
from custom_type.gait_seqs_type   import GaitIdxSeqsType


class ActionSqsType(WalkDirType):

    __slots__ = ("ctraj_acts_dic","vpump_acts_dic","_iter_idx_" )
    CTRAJ_IDX_NAMS = ["CTRAJ_IDX_SEQS_FWD" ,"CTRAJ_IDX_SEQS_BKD",
                      "CTRAJ_IDX_SEQS_ROTL","CTRAJ_IDX_SEQS_ROTR"]

    def __init__(self,act_sqs_cfg:dict=None):
        
        self.ctraj_acts_dic = {
                self.WLK_FWD : GaitIdxSeqsType(),self.WLK_BKWD: GaitIdxSeqsType(),
                self.ROT_LFT : GaitIdxSeqsType(),self.ROT_RHT : GaitIdxSeqsType()}
        
        if act_sqs_cfg is not None:
            self.set_by_act_dic(act_sqs_cfg)
    
    def acton_sqs_loader(self,act_sqs_fil:str="./config/action_sqs_cfg.json"):

        out_file    = open(act_sqs_fil, "r")
        act_sqs_dic = json.load(out_file)
        
        self.set_by_act_dic(act_sqs_dic)

    def set_by_act_dic(self,act_sqs_dic:dict=None):
        """
        Action of legs and valve-pumps type: 
        CTRAJ_IDX_SEQS_FWD: Stores cartesian trajectory's index
        {
        "CTRAJ_IDX_SEQS_FWD": 
            {  
            "0" : {"rm": 0,"rf": 0,"lf": 0,"lm": 0,"lb": 0,"rb": 0 ,"name": "t0  step1 move lfnt leg" },
            "1" : {"rm": 0,"rf": 0,"lf": 1,"lm": 0,"lb": 0,"rb": 0 ,"name": "t1  step1 move lfnt leg" },
            ...
            "15": {"rm": 3,"rf": 3,"lf": 3,"lm": 3,"lb": 3,"rb": 3 ,"name": "t15  step4 move bak leg" },
            "16": {"rm": 0,"rf": 0,"lf": 0,"lm": 0,"lb": 0,"rb": 0 ,"name": "t16  step5 move body"    }
            },
        ... 
        }
        """
        
        for (idx,traj_nam) in enumerate(self.CTRAJ_IDX_NAMS):
            self.ctraj_acts_dic[self.WLK_LST[idx]].set_by_strkey(act_sqs_dic[traj_nam])
            
    def get_current_acts(self)->GaitIdxSeqsType:
        cur_dir = self.get_cur_dir()
        return deepcopy(self.ctraj_acts_dic[cur_dir])
        
    def get_fwd_acts(self)->GaitIdxSeqsType:
        return deepcopy(self.ctraj_acts_dic[self.WLK_FWD])

    def get_bak_acts(self)->GaitIdxSeqsType:
        return deepcopy(self.ctraj_acts_dic[self.WLK_BKWD])
    
    def get_rotl_acts(self)->GaitIdxSeqsType:
        return deepcopy(self.ctraj_acts_dic[self.ROT_LFT])
    
    def get_rotr_acts(self)->GaitIdxSeqsType:
        return deepcopy(self.ctraj_acts_dic[self.ROT_RHT])
    
    def get_acts_by_idx(self,idx:int)->GaitIdxSeqsType:
        dir_nam = self.WLK_LST[idx%len(self.WLK_LST)]
        return deepcopy(self.ctraj_acts_dic[dir_nam])

    def get_acts_by_nam(self,dir_nam:WalkDirType)->GaitIdxSeqsType:
        cta = deepcopy(self.ctraj_acts_dic[dir_nam.get_cur_dir()])
        return cta
    
    def __iter__(self):
        self._iter_idx_ = 0
        return self
    
    def __next__(self)->GaitIdxSeqsType:
        if self._iter_idx_ < len(self.WLK_LST):
            cta = self.get_acts_by_idx(self._iter_idx_)
            self._iter_idx_ += 1
            return cta
        else:
            raise StopIteration
        
        
if __name__ == "__main__":
    acq = ActionSqsType()
    acq.acton_sqs_loader()

    for idx,act in enumerate(acq):
        print(idx,act,"\n------\n")