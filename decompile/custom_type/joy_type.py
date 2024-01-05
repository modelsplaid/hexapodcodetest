import  json
from    warnings        import warn
from    typing          import List, Union
from    copy            import deepcopy

class JoyType:
    __slots__ = ("joy_dic","name")
    def __init__(self, name:str="",joy_dic:dict=None):

        # Check type
        if joy_dic is not None: 
            if (isinstance(joy_dic,dict) == False or isinstance(name,str)== False):
                raise NameError('fatal error: Incorrect arguments type')
            self.joy_dic = joy_dic
        else:
            joy_dic_tplt = {
                "found"      :"yes" ,"connected"  :"yes","t_stamp"   :0,
                "dpadUp"     :0     ,"dpadDown"   :0    ,"dpadLeft"  :0,
                "dpadRight"  :0     ,"BackBtn"    :0    ,"GuidBtn"   :0,
                "StartBtn"   :0     ,"ABtn"       :0    ,"BBtn"      :0,
                "XBtn"       :0     ,"YBtn"       :0    ,"LftBumpBtn":0,    
                "RhtBumpBtn" :0     ,"LftTrigBtn" :0    ,"RhtTrigBtn":0,
                "LftStickBtn":0     ,"RhtStickBtn":0    ,"NumDevice" :0,
                "LftStick"   :{"x":0,"y":0},
                "RhtStick"   :{"x":0,"y":0},
                }
            self.joy_dic = joy_dic_tplt
        self.name = name

    def set_found(self,val):
        self.joy_dic["found"] = val

    def set_connected(self,val):
        self.joy_dic["connected"] = val
        self.joy_dic["NumDevice"] = 1

    def set_tstamp(self,val):
        self.joy_dic["t_stamp"] = val

    def set_dpad_up(self,val):
        self.joy_dic["dpadUp"] = val

    def set_dpad_down(self,val):
        self.joy_dic["dpadDown"] = val

    def set_dpad_left(self,val):
        self.joy_dic["dpadLeft"] = val

    def set_dpad_right(self,val):
        self.joy_dic["dpadRight"] = val

    def set_back(self,val):
        self.joy_dic["BackBtn"] = val

    def set_guide(self,val):
        self.joy_dic["GuidBtn"] = val

    def set_start(self,val):
        self.joy_dic["StartBtn"] = val

    def set_lft_stick_btn(self,val):
        self.joy_dic["LftStickBtn"] = val

    def set_rht_stick_btn(self,val):
        self.joy_dic["RhtStickBtn"] = val

    def set_a_btn(self,val):
        self.joy_dic["ABtn"] = val

    def set_b_btn(self,val):
        self.joy_dic["BBtn"] = val

    def set_x_btn(self,val):
        self.joy_dic["XBtn"] = val

    def set_y_btn(self,val):
        self.joy_dic["YBtn"] = val

    def set_lft_bumper(self,val):
        self.joy_dic["LftBumpBtn"] = val

    def set_rht_bumper(self,val):
        self.joy_dic["RhtBumpBtn"] = val

    def set_lft_trigger(self,val):
        self.joy_dic["LftTrigBtn"] = val

    def set_rht_trigger(self,val):
        self.joy_dic["RhtTrigBtn"] = val

    def set_lft_stick(self,val1,val2):
        self.joy_dic["LftStick"]["x"] = val1
        self.joy_dic["LftStick"]["y"] = val2

    def set_rht_stick(self,val1,val2):
        self.joy_dic["RhtStick"]["x"] = val1
        self.joy_dic["RhtStick"]["y"] = val2

    def set_joydic_by_json(self,json_joydic:str):
        joydic = json.loads(json_joydic)
        self.joy_dic = joydic

    def get_dpad_up(self):
        return deepcopy(self.joy_dic["dpadUp"])
    
    def get_dpad_down(self):
        return deepcopy(self.joy_dic["dpadDown"])
    
    def get_dpad_left(self):
        return deepcopy(self.joy_dic["dpadLeft"])
    
    def get_dpad_right(self):
        return deepcopy(self.joy_dic["dpadRight"])
    
    def get_back(self):
        return deepcopy(self.joy_dic["BackBtn"])
    
    def get_guide(self):
        return deepcopy(self.joy_dic["GuidBtn"])
    
    def get_start(self):
        return deepcopy(self.joy_dic["StartBtn"])
    
    def get_lft_stick_btn(self):
        return deepcopy(self.joy_dic["LftStickBtn"])
    
    def get_rht_stick_btn(self):
        return deepcopy(self.joy_dic["RhtStickBtn"])
    
    def get_a_btn(self):
        return deepcopy(self.joy_dic["ABtn"])
    
    def get_b_btn(self):
        return deepcopy(self.joy_dic["BBtn"])
    
    def get_x_btn(self):
        return deepcopy(self.joy_dic["XBtn"])
    
    def get_y_btn(self):
        return deepcopy(self.joy_dic["YBtn"])
    
    def get_lft_bumper(self):
        return deepcopy(self.joy_dic["LftBumpBtn"])
    
    def get_rht_bumper(self):
        return deepcopy(self.joy_dic["RhtBumpBtn"])
    
    def get_lft_trigger(self):
        return deepcopy(self.joy_dic["LftTrigBtn"])
    
    def get_rht_trigger(self):
        return deepcopy(self.joy_dic["RhtTrigBtn"])
    
    def get_lft_stick(self):
        x = self.joy_dic["LftStick"]["x"]
        y = self.joy_dic["LftStick"]["y"]
        return [x,y]
    
    def get_rht_stick(self):
        x = self.joy_dic["RhtStick"]["x"]
        y = self.joy_dic["RhtStick"]["y"]
        return [x,y]

    def get_joy_dic(self):
        return deepcopy(self.joy_dic)

    def get_json_joydic(self):
        joydic = self.get_joy_dic()
        json_joydic = json.dumps(joydic)
        return json_joydic

    def get_tstamp(self):
        return self.joy_dic["t_stamp"]

    def get_connected(self):
        return (self.joy_dic["connected"])

    def get_found(self):
        return self.joy_dic["found"]
    
    def __eq__(self,obj):
        """
        type obj: JoyType   
        """
        if isinstance(obj,JoyType) == False: 
            return False
        
        if  self.joy_dic["found"      ] != obj.joy_dic["found"      ] or \
            self.joy_dic["connected"  ] != obj.joy_dic["connected"  ] or \
            self.joy_dic["dpadUp"     ] != obj.joy_dic["dpadUp"     ] or \
            self.joy_dic["dpadDown"   ] != obj.joy_dic["dpadDown"   ] or \
            self.joy_dic["dpadLeft"   ] != obj.joy_dic["dpadLeft"   ] or \
            self.joy_dic["dpadRight"  ] != obj.joy_dic["dpadRight"  ] or \
            self.joy_dic["BackBtn"    ] != obj.joy_dic["BackBtn"    ] or \
            self.joy_dic["GuidBtn"    ] != obj.joy_dic["GuidBtn"    ] or \
            self.joy_dic["StartBtn"   ] != obj.joy_dic["StartBtn"   ] or \
            self.joy_dic["ABtn"       ] != obj.joy_dic["ABtn"       ] or \
            self.joy_dic["BBtn"       ] != obj.joy_dic["BBtn"       ] or \
            self.joy_dic["XBtn"       ] != obj.joy_dic["XBtn"       ] or \
            self.joy_dic["YBtn"       ] != obj.joy_dic["YBtn"       ] or \
            self.joy_dic["LftBumpBtn" ] != obj.joy_dic["LftBumpBtn" ] or \
            self.joy_dic["RhtBumpBtn" ] != obj.joy_dic["RhtBumpBtn" ] or \
            self.joy_dic["LftTrigBtn" ] != obj.joy_dic["LftTrigBtn" ] or \
            self.joy_dic["RhtTrigBtn" ] != obj.joy_dic["RhtTrigBtn" ] or \
            self.joy_dic["LftStickBtn"] != obj.joy_dic["LftStickBtn"] or \
            self.joy_dic["RhtStickBtn"] != obj.joy_dic["RhtStickBtn"] or \
            self.joy_dic["LftStick"   ] != obj.joy_dic["LftStick"   ] or \
            self.joy_dic["RhtStick"   ] != obj.joy_dic["RhtStick"   ] or \
            self.joy_dic["NumDevice"  ] != obj.joy_dic["NumDevice"  ]:

            return False 
        else: 
            return True
    def form_str(self):

        def format_str(key,val,key_len=13,val_len=5):
            key_str = str(key)+": "
            val_str = str(val)
            cmp_key = key_str+(key_len-len(key_str))*' '
            cmp_val = val_str+(val_len-len(val_str))*' '

            return (cmp_key+cmp_val)

        full_str = ''
        for i,key in enumerate(self.joy_dic):
            full_str = full_str+format_str(key,self.joy_dic[key])
            if i%3==2:
                full_str = full_str+"\n"
        
        full_str = "---"+self.name + ":\n"+ full_str
        return full_str

    
    def __str__(self):
        return self.form_str()
        

if __name__ == '__main__':
    jt = JoyType()
    jt2 = JoyType()
    jt2.set_back(1)
    print(jt==jt2)
    