import json 
import sys
from copy       import deepcopy
sys.path.append("../")


class IKPropsType:  
    __slots__ = ("ik_param_dic","name")

    def __init__(self, name:str="",bdy_ik_dic:dict=None):

        if (isinstance(name,str)== False):
            raise NameError('fatal error: Incorrect arguments type')
        
        if bdy_ik_dic is not None and isinstance(bdy_ik_dic,dict) == False:
                raise NameError('fatal error: Incorrect arguments type')

        bdy_ik_dic_tplt  = {
            "BDY_IK_PARAMS": 
            {
            "cob_tran_wgnd"   :{"tx":0,"ty":0  ,"tz":80},
            "cob_rota_wgnd"   :{"r":0 ,"p":0   ,"y":0  }, 
            "leg_conta_shift" :{"tx":0,"ty":110,"tz":0 }
            }
        }

        if bdy_ik_dic == None: 
            self.ik_param_dic = bdy_ik_dic_tplt
        else: 
            self.ik_param_dic = deepcopy(bdy_ik_dic)

        self.name = name

    def get_gait_param_dic(self):
        """
        Set a given ik_param_dic
        """
        return deepcopy(self.ik_param_dic)
    

    def get_t_xyz(self):
        """
        Return [tx,ty,tz]self.bdy_leg_pts
        """

        tx = self.ik_param_dic["BDY_IK_PARAMS"]["cob_tran_wgnd"]["tx"]
        ty = self.ik_param_dic["BDY_IK_PARAMS"]["cob_tran_wgnd"]["ty"]
        tz = self.ik_param_dic["BDY_IK_PARAMS"]["cob_tran_wgnd"]["tz"]

        return [tx,ty,tz]
    
    def get_r_rpy(self):
        """
        Get roll pitch yaw rotation angle
        return: [r_deg,p_deg,y_deg]
        """
        r_deg = self.ik_param_dic["BDY_IK_PARAMS"]["cob_rota_wgnd"]["r"]
        p_deg = self.ik_param_dic["BDY_IK_PARAMS"]["cob_rota_wgnd"]["p"]
        y_deg = self.ik_param_dic["BDY_IK_PARAMS"]["cob_rota_wgnd"]["y"] 

        return [r_deg,p_deg,y_deg]
    
    def get_leg_conta_shift(self):
        """
        Return: [shift_x,shift_y,shift_z]
        """
        leg_conta_shift = [0,0,0]
        leg_conta_shift[0] = self.ik_param_dic["BDY_IK_PARAMS"]["leg_conta_shift"]["tx"]
        leg_conta_shift[1] = self.ik_param_dic["BDY_IK_PARAMS"]["leg_conta_shift"]["ty"]
        leg_conta_shift[2] = self.ik_param_dic["BDY_IK_PARAMS"]["leg_conta_shift"]["tz"]
        return leg_conta_shift

    def set_t_xyz(self,tx=0,ty=0,tz=0):
        self.ik_param_dic["BDY_IK_PARAMS"]["cob_tran_wgnd"]["tx"] = tx
        self.ik_param_dic["BDY_IK_PARAMS"]["cob_tran_wgnd"]["ty"] = ty
        self.ik_param_dic["BDY_IK_PARAMS"]["cob_tran_wgnd"]["tz"] = tz

    def set_ik_param_dic(self,ik_param_dic:dict=None):
        """
        Set a given ik_param_dic
        """
        self.ik_param_dic = deepcopy(ik_param_dic)

    def set_r_rpy(self,r=0,p=0,y=0):
        """
        Set roll pitch yaw rotation angle
        """
        self.ik_param_dic["BDY_IK_PARAMS"]["cob_rota_wgnd"]["r"] = r
        self.ik_param_dic["BDY_IK_PARAMS"]["cob_rota_wgnd"]["p"] = p
        self.ik_param_dic["BDY_IK_PARAMS"]["cob_rota_wgnd"]["y"] = y 


    def __str__(self):

        ik_param_dic = self.ik_param_dic["BDY_IK_PARAMS"] 
        key_arr = list(ik_param_dic.keys())
        
        str_pt = ""
        for key in key_arr:
            lenk = len(key)
            cmp = " "*(16-lenk)
            str_pt = str_pt + key+cmp+": "+ str(ik_param_dic[key])+"\n"

        return str_pt
    
    def __eq__(self, obj):
        """
        Compare each value, if all same, return true, otherwise return false. 
        If type is not same, return false
        """
        if isinstance(obj,IKPropsType) == False: 
            return False
        
        if  self.ik_param_dic["BDY_IK_PARAMS"]["cob_tran_wgnd"]["tx"]!= obj.ik_param_dic["BDY_IK_PARAMS"]["cob_tran_wgnd"]["tx"] or\
            self.ik_param_dic["BDY_IK_PARAMS"]["cob_tran_wgnd"]["ty"]!= obj.ik_param_dic["BDY_IK_PARAMS"]["cob_tran_wgnd"]["ty"] or\
            self.ik_param_dic["BDY_IK_PARAMS"]["cob_tran_wgnd"]["tz"]!= obj.ik_param_dic["BDY_IK_PARAMS"]["cob_tran_wgnd"]["tz"] or\
            self.ik_param_dic["BDY_IK_PARAMS"]["cob_rota_wgnd"]["r" ]!= obj.ik_param_dic["BDY_IK_PARAMS"]["cob_rota_wgnd"]["r" ] or\
            self.ik_param_dic["BDY_IK_PARAMS"]["cob_rota_wgnd"]["p" ]!= obj.ik_param_dic["BDY_IK_PARAMS"]["cob_rota_wgnd"]["p" ] or\
            self.ik_param_dic["BDY_IK_PARAMS"]["cob_rota_wgnd"]["y" ]!= obj.ik_param_dic["BDY_IK_PARAMS"]["cob_rota_wgnd"]["y" ]   :

                return False

        else: 
            return True

if __name__ == "__main__":
    bdy_ik_cfg_fil     = open("../config/bdy_ik_cfg.json", "r")
    BDY_IK_CFG_DIC     = json.load(bdy_ik_cfg_fil)
    bdyparam = IKPropsType("bdy_ik",BDY_IK_CFG_DIC)
    bdyparam2 = IKPropsType("bdy_ik",BDY_IK_CFG_DIC)
    print(bdyparam)

    print(bdyparam == bdyparam2)

    print(bdyparam.get_r_rpy())
    print(bdyparam.get_t_xyz())
    print(bdyparam.get_leg_conta_shift())

