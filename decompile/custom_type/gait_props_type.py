"""
Inverse Kinematics Algorithm: 

The inverse kinematics algorithm is to solve this problem: 
Given robot's center height, robot's rotation angle, legs' x-y-axis shift, compute legs angle. 

# How does it work: 

## Definition 

### 1. robot center height: 

Robot center height is the distance form cob (see below diagram) to ground level
```
                 front
              *---*---*
             /   y^    \     
            /     |     \    
           /      |      \   
 left     *------cob--->--*      right            
           \      |    x /
            \     |     / 
             \    |    /  
              *---*---*    
```
### 2. robot's rotation angle
Robot's x,y,z rotation with respect to gnd (ground center coordinate)

### 3. tx-ty-tz body shift
One robot's pose consist of  three-position and three rotation. 
Even if we defined rotation angle, and height, we still have two undefined parameters. 

The x-shift is defined this: 
               
       legs' body point shift
                front
       *---------------------*     
       |                     |  
       |   *-------------*   |    
       |   |    y^       |   |   
       *   |     |       |   *   
       |   |     |       |   |   
       |   *     *--->   *   |                  
       |   |    gnd  x   |   |
       *---|-------------|---* 
           |             |     
           *-------------*       
       \_/                \_/
       x-shift            x-shift


The y-shift is defined this: 


      legs' body point shift
               front
      *----------*----------* \    
      |                     |  | y-shift
      |   *-------------*   | /   
      |   |             |   |   
      *   |             |   *   
      |   |             |   |   
      |   *             *   |                  
      |   |             |   |
      *---|-------------|---* \
          |             |      | y-shift
          *-------------*     /  

## 4. leg_conta_shift: 
    leg_conta_shift is the shift of legs' contact points

    X-shift: X-shift is POSITIVE: left ,and rght legs EXPAND in left  and rght direction
             X-shift is NEGATIVE: left ,and rght legs SHRINK in left  and rght direction     
    y-shift: y-shift is POSITIVE: front,and back legs EXPAND in front and back direction
             y-shift is NEGATIVE: front,and back legs SHRINK in front and back direction 
    z-shift: Moves leg up and down. Note this is kind of redundant, since we already defined the bot's height
             So this should always set as 0 
    

    legs' contact points w.r.t gnd 

               front
      *----------*----------* \    
      |                     |  | y-shift 
      |   *-------------*   | /   
      |   |             |   |   
      |   |             |   |   
      |   |             |   |   
      *   *             *   *                  
      |   |             |   |
      |   |             |   |
      |   |             |   |   
      |   *-------------*   |\   
      |                     | | y-shift 
      *---------------------*/ 
                        \__/
                       x-shift
"""


import json 
import time
import sys
sys.path.append("../")
from typing     import List, Union
from copy       import deepcopy

class GaitPropsType:  
    __slots__ = ("gait_param_dic","name")

    def __init__(self, name:str="",gait_param_dic:dict=None):

        if (isinstance(name,str)== False):
            raise NameError('fatal error: Incorrect arguments type')
        
        if gait_param_dic is not None and isinstance(gait_param_dic,dict) == False:
                raise NameError('fatal error: Incorrect arguments type')

        gait_param_dic_tmplt  = {
                    "hip_swing_mm"    :{"default":30  ,"max":100,"min":1   },
                    "lift_swing_mm"   :{"default":10  ,"max":100,"min":1   },
                    "step_count"      :{"default":4   ,"max":6  ,"min":0   },    
                    "rot_swing_deg"   :{"default":5   ,"max":-10,"min":10  },
                    "stanc_period_ms" :{"default":200 ,"max":900,"min":100 },
                    "swing_period_ms" :{"default":200 ,"max":900,"min":100 },
                    "vpump_period_ms" :{"default":200 ,"max":900,"min":100 }                    
                    }

        if gait_param_dic == None: 
            self.gait_param_dic = gait_param_dic_tmplt
        else: 
            self.gait_param_dic = deepcopy(gait_param_dic)

        self.name = name

    def set_gait_param_dic(self,gait_param_dic:dict=None):
        """
        Set a given gait_param_dic
        """
        self.gait_param_dic = deepcopy(gait_param_dic)
    
    def set_swing_dis(self,hip_swing_mm=0,lift_swing_mm=0):
        """
        When robot move forward, define legs' swing distance
        """
        self.gait_param_dic["hip_swing_mm" ]["default"] = hip_swing_mm
        self.gait_param_dic["lift_swing_mm"]["default"] = lift_swing_mm

    def set_rot_swing_agl(self,rot_swing_deg=5):
        """
        When robot rotate, define legs' swing deg  
        """
        self.gait_param_dic["rot_swing_deg"]["default"] = rot_swing_deg

    def set_stanc_prid(self,stanc_perid_ms:float=0):
        self.gait_param_dic["stanc_period_ms"]["default"] = stanc_perid_ms

    def set_swing_prid(self,swing_perid_ms:float=0):
        self.gait_param_dic["swing_period_ms"]["default"] = swing_perid_ms

    def set_vpump_prid(self,vpump_perid_ms:float=0):
        self.gait_param_dic["vpump_period_ms"]["default"] = vpump_perid_ms
        
    def get_gait_param_dic(self):
        """
        Set a given gait_param_dic
        """
        return deepcopy(self.gait_param_dic)

    def get_swing_dis(self):
        """
        When robot move forward, define legs' swing length  
        return [hip_swing_mm,lift_swing_mm]
        """
        hip_swing_mm  = self.gait_param_dic["hip_swing_mm" ]["default"] 
        lift_swing_mm = self.gait_param_dic["lift_swing_mm"]["default"] 

        return [hip_swing_mm,lift_swing_mm]
    
    def get_rot_swing_agl(self):
        """
        When robot rotate, define legs' swing deg  
        """
        return self.gait_param_dic["rot_swing_deg"]["default"]

    def get_max_props(self):
        """
        Get properties for all max values
        Return: in the list of [hip_swin,lift_swin,stp_cnt,spd_prid]
        """
        hip_s = self.gait_param_dic["hip_swing_mm"   ]["max"]
        lft_s = self.gait_param_dic["lift_swing_mm"  ]["max"]
        stp_c = self.gait_param_dic["step_count"     ]["max"]
        spd_p = self.gait_param_dic["stanc_period_ms"]["max"]
        rot_s = self.gait_param_dic["rot_swing_deg"  ]["max"]

        return [hip_s,lft_s,rot_s,stp_c,spd_p]

    def get_min_props(self):
        """
        Get properties for all min values
        Return: in the list of [hip_swin,lift_swin,stp_cnt,spd_prid]
        """
        hip_s = self.gait_param_dic["hip_swing_mm"   ]["min"]
        lft_s = self.gait_param_dic["lift_swing_mm"  ]["min"]
        stp_c = self.gait_param_dic["step_count"     ]["min"]
        spd_p = self.gait_param_dic["stanc_period_ms"]["min"]
        rot_s = self.gait_param_dic["rot_swing_deg"  ]["min"]

        return [hip_s,lft_s,rot_s,stp_c,spd_p]

    def get_dft_props(self):
        """
        Get properties for all default values
        Return: in the list of [hip_swin,lift_swin,stp_cnt,spd_prid]
        """
        hip_s = self.gait_param_dic["hip_swing_mm"   ]["default"]
        lft_s = self.gait_param_dic["lift_swing_mm"  ]["default"]
        stp_c = self.gait_param_dic["step_count"     ]["default"]
        spd_p = self.gait_param_dic["stanc_period_ms"]["default"]
        rot_s = self.gait_param_dic["rot_swing_deg"  ]["default"]
        return [hip_s,lft_s,rot_s,stp_c,spd_p]

    def get_stanc_prid(self):
        return self.gait_param_dic["stanc_period_ms"]["default"] 

    def get_swing_prid(self):
        return self.gait_param_dic["swing_period_ms"]["default"] 

    def get_vpump_prid(self):
        return self.gait_param_dic["vpump_period_ms"]["default"]

    def __str__(self):
         
        key_arr = list(self.gait_param_dic.keys())
        
        str_pt = ""
        for key in key_arr:
            lenk = len(key)
            cmp = " "*(16-lenk)
            str_pt = str_pt + key+cmp+": "+ str(self.gait_param_dic[key])+"\n"

        return str_pt
    
    def __eq__(self, obj):
        """
        Compare each value, if all same, return true, otherwise return false. 
        If type is not same, return false
        """
        if isinstance(obj,GaitPropsType) == False: 
            return False
        
        if  self.gait_param_dic["hip_swing_mm" ]["default"] != obj.gait_param_dic["hip_swing_mm" ]["default"] or\
            self.gait_param_dic["lift_swing_mm"]["default"] != obj.gait_param_dic["lift_swing_mm"]["default"] or\
            self.gait_param_dic["step_count"   ]["default"] != obj.gait_param_dic["step_count"   ]["default"] or\
            self.gait_param_dic["rot_swing_deg"]["default"] != obj.gait_param_dic["rot_swing_deg"]["default"]:           
                return False

        else: 
            return True
    
if __name__ == "__main__":
    # HOW to run it: 
    # 1. Go to project's current directory
    # 2. python3 gait_props_type.py
    gp = GaitPropsType("gp")
    print(gp)
    gp2 = GaitPropsType("gp2")
    gpcp = deepcopy(gp)
    print("gp==gp2: "+str(gp==gp2))
    print("gp==gpcp: "+str(gp==gpcp))
    print("gp==3: "+str(gp==3))



