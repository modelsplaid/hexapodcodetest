import sys
from typing     import List,Union
from copy       import deepcopy 

class BotCmuMsgType:
    __slots__ = ("cmu_msg_dic","name")
    num_legs    = 6
    num_svos    = 18

    OFF_VALV    = 0 
    ON_VALV     = 1
    NO_ACT_VALV = 2

    ssvo_head   = "serial_servo_"
    leg_nams    = ["right-middle","right-front","left-front",
                   "left-middle" ,"left-back"  ,"right-back"]
    
    def __init__(self, name:str="",cmu_msg_dic:dict=None):
        if isinstance(name,str)== False:
            raise NameError('fatal error: Incorrect arguments type')
            
        if cmu_msg_dic is not None and isinstance(cmu_msg_dic,dict) == False:
            raise NameError('fatal error: Incorrect arguments type')
        
        cmu_msg_dic_tmplt = {
            "serial_servos": {
                "serial_servo_1": {
                    "device_id"       : 1    ,"servo_name"        : "left-back-coxa","time_stamp":0 ,
                    "send_servo_valid": False,"send_servo_pos_val": 0,"send_servo_pos_stats": "","send_servo_speed_val": 0,"send_servo_speed_stats": "","send_servo_torque_val": 0,"send_servo_torque_stats": "" ,
                    "recv_servo_valid": False,"recv_servo_pos_val": 0,"recv_servo_pos_stats": "","recv_servo_speed_val": 0,"recv_servo_speed_stats": "","recv_servo_torque_val": 0,"recv_servo_torque_stats": ""},
                "serial_servo_2": {
                    "device_id"       : 2    ,"servo_name"        : "left-back-femur","time_stamp":0,    
                    "send_servo_valid": False,"send_servo_pos_val": 0,"send_servo_pos_stats": "","send_servo_speed_val": 0,"send_servo_speed_stats": "","send_servo_torque_val": 0,"send_servo_torque_stats": "",
                    "recv_servo_valid": False,"recv_servo_pos_val": 0,"recv_servo_pos_stats": "","recv_servo_speed_val": 0,"recv_servo_speed_stats": "","recv_servo_torque_val": 0,"recv_servo_torque_stats": ""},
                "serial_servo_3": {
                    "device_id"       : 3,    "servo_name"        : "left-back-tibia","time_stamp":0,
                    "send_servo_valid": False,"send_servo_pos_val": 0,"send_servo_pos_stats": "","send_servo_speed_val": 0,"send_servo_speed_stats": "","send_servo_torque_val": 0,"send_servo_torque_stats": "",
                    "recv_servo_valid": False,"recv_servo_pos_val": 0,"recv_servo_pos_stats": "","recv_servo_speed_val": 0,"recv_servo_speed_stats": "","recv_servo_torque_val": 0,"recv_servo_torque_stats": ""},
                "serial_servo_4": {
                    "device_id"       : 4    ,"servo_name"        : "left-middle-coxa","time_stamp": 0,
                    "send_servo_valid": False,"send_servo_pos_val": 0,"send_servo_pos_stats": "","send_servo_speed_val": 0,"send_servo_speed_stats": "","send_servo_torque_val": 0,"send_servo_torque_stats": "",
                    "recv_servo_valid": False,"recv_servo_pos_val": 0,"recv_servo_pos_stats": "","recv_servo_speed_val": 0,"recv_servo_speed_stats": "","recv_servo_torque_val": 0,"recv_servo_torque_stats": ""},
                "serial_servo_5": {
                    "device_id"       : 5,"servo_name"            : "left-middle-femur","time_stamp": 0,
                    "send_servo_valid": False,"send_servo_pos_val": 0,"send_servo_pos_stats": "","send_servo_speed_val": 0,"send_servo_speed_stats": "","send_servo_torque_val": 0,"send_servo_torque_stats": "",
                    "recv_servo_valid": False,"recv_servo_pos_val": 0,"recv_servo_pos_stats": "","recv_servo_speed_val": 0,"recv_servo_speed_stats": "","recv_servo_torque_val": 0,"recv_servo_torque_stats": ""},
                "serial_servo_6": {
                    "device_id"       : 6,"servo_name"            : "left-middle-tibia","time_stamp": 0,
                    "send_servo_valid": False,"send_servo_pos_val": 0,"send_servo_pos_stats": "","send_servo_speed_val": 0,"send_servo_speed_stats": "","send_servo_torque_val": 0,"send_servo_torque_stats": "",
                    "recv_servo_valid": False,"recv_servo_pos_val": 0,"recv_servo_pos_stats": "","recv_servo_speed_val": 0,"recv_servo_speed_stats": "","recv_servo_torque_val": 0,"recv_servo_torque_stats": ""},
                "serial_servo_7": {
                    "device_id"       : 7,"servo_name"            : "left-front-coxa","time_stamp": 0,
                    "send_servo_valid": False,"send_servo_pos_val": 0,"send_servo_pos_stats": "","send_servo_speed_val": 0,"send_servo_speed_stats": "","send_servo_torque_val": 0,"send_servo_torque_stats": "",
                    "recv_servo_valid": False,"recv_servo_pos_val": 0,"recv_servo_pos_stats": "","recv_servo_speed_val": 0,"recv_servo_speed_stats": "","recv_servo_torque_val": 0,"recv_servo_torque_stats": ""},
                "serial_servo_8": {
                    "device_id"       : 8,"servo_name"            : "left-front-femur","time_stamp": 0,
                    "send_servo_valid": False,"send_servo_pos_val": 0,"send_servo_pos_stats": "","send_servo_speed_val": 0,"send_servo_speed_stats": "","send_servo_torque_val": 0,"send_servo_torque_stats": "",
                    "recv_servo_valid": False,"recv_servo_pos_val": 0,"recv_servo_pos_stats": "","recv_servo_speed_val": 0,"recv_servo_speed_stats": "","recv_servo_torque_val": 0,"recv_servo_torque_stats": ""},
                "serial_servo_9": {
                    "device_id"       : 9,"servo_name"            : "left-front-tibia","time_stamp": 0,
                    "send_servo_valid": False,"send_servo_pos_val": 0,"send_servo_pos_stats": "","send_servo_speed_val": 0,"send_servo_speed_stats": "","send_servo_torque_val": 0,"send_servo_torque_stats": "",
                    "recv_servo_valid": False,"recv_servo_pos_val": 0,"recv_servo_pos_stats": "","recv_servo_speed_val": 0,"recv_servo_speed_stats": "","recv_servo_torque_val": 0,"recv_servo_torque_stats": ""},
                "serial_servo_10": {
                    "device_id"       : 10,"servo_name"           : "right-back-coxa","time_stamp": 0,
                    "send_servo_valid": False,"send_servo_pos_val": 0,"send_servo_pos_stats": "","send_servo_speed_val": 0,"send_servo_speed_stats": "","send_servo_torque_val": 0,"send_servo_torque_stats": "",
                    "recv_servo_valid": False,"recv_servo_pos_val": 0,"recv_servo_pos_stats": "","recv_servo_speed_val": 0,"recv_servo_speed_stats": "","recv_servo_torque_val": 0,"recv_servo_torque_stats": ""},
                "serial_servo_11": {
                    "device_id"       : 11,"servo_name"           : "right-back-femur","time_stamp": 0,
                    "send_servo_valid": False,"send_servo_pos_val": 0,"send_servo_pos_stats": "","send_servo_speed_val": 0,"send_servo_speed_stats": "","send_servo_torque_val": 0,"send_servo_torque_stats": "",
                    "recv_servo_valid": False,"recv_servo_pos_val": 0,"recv_servo_pos_stats": "","recv_servo_speed_val": 0,"recv_servo_speed_stats": "","recv_servo_torque_val": 0,"recv_servo_torque_stats": ""},
                "serial_servo_12": {
                    "device_id"       : 12,"servo_name"           : "right-back-tibia","time_stamp": 0,
                    "send_servo_valid": False,"send_servo_pos_val": 0,"send_servo_pos_stats": "","send_servo_speed_val": 0,"send_servo_speed_stats": "","send_servo_torque_val": 0,"send_servo_torque_stats": "",
                    "recv_servo_valid": False,"recv_servo_pos_val": 0,"recv_servo_pos_stats": "","recv_servo_speed_val": 0,"recv_servo_speed_stats": "","recv_servo_torque_val": 0,"recv_servo_torque_stats": ""},
                "serial_servo_13": {
                    "device_id"       : 13,"servo_name"           : "right-middle-coxa","time_stamp": 0,
                    "send_servo_valid": False,"send_servo_pos_val": 0,"send_servo_pos_stats": "","send_servo_speed_val": 0,"send_servo_speed_stats": "","send_servo_torque_val": 0,"send_servo_torque_stats": "",
                    "recv_servo_valid": False,"recv_servo_pos_val": 0,"recv_servo_pos_stats": "","recv_servo_speed_val": 0,"recv_servo_speed_stats": "","recv_servo_torque_val": 0,"recv_servo_torque_stats": ""},
                "serial_servo_14": {
                    "device_id"       : 14,"servo_name"           : "right-middle-femur","time_stamp": 0,
                    "send_servo_valid": False,"send_servo_pos_val": 0,"send_servo_pos_stats": "","send_servo_speed_val": 0,"send_servo_speed_stats": "","send_servo_torque_val": 0,"send_servo_torque_stats": "",
                    "recv_servo_valid": False,"recv_servo_pos_val": 0,"recv_servo_pos_stats": "","recv_servo_speed_val": 0,"recv_servo_speed_stats": "","recv_servo_torque_val": 0,"recv_servo_torque_stats": ""},
                "serial_servo_15": {
                    "device_id"       : 15,"servo_name"           : "right-middle-tibia","time_stamp": 0,
                    "send_servo_valid": False,"send_servo_pos_val": 0,"send_servo_pos_stats": "","send_servo_speed_val": 0,"send_servo_speed_stats": "","send_servo_torque_val": 0,"send_servo_torque_stats": "",
                    "recv_servo_valid": False,"recv_servo_pos_val": 0,"recv_servo_pos_stats": "","recv_servo_speed_val": 0,"recv_servo_speed_stats": "","recv_servo_torque_val": 0,"recv_servo_torque_stats": ""},
                "serial_servo_16": {
                    "device_id"       : 16,"servo_name"           : "right-front-coxa","time_stamp": 0,
                    "send_servo_valid": False,"send_servo_pos_val": 0,"send_servo_pos_stats": "","send_servo_speed_val": 0,"send_servo_speed_stats": "","send_servo_torque_val": 0,"send_servo_torque_stats": "",
                    "recv_servo_valid": False,"recv_servo_pos_val": 0,"recv_servo_pos_stats": "","recv_servo_speed_val": 0,"recv_servo_speed_stats": "","recv_servo_torque_val": 0,"recv_servo_torque_stats": ""},
                "serial_servo_17": {
                    "device_id"       : 17,"servo_name"           : "right-front-femur","time_stamp": 0,
                    "send_servo_valid": False,"send_servo_pos_val": 0,"send_servo_pos_stats": "","send_servo_speed_val": 0,"send_servo_speed_stats": "","send_servo_torque_val": 0,"send_servo_torque_stats": "",
                    "recv_servo_valid": False,"recv_servo_pos_val": 0,"recv_servo_pos_stats": "","recv_servo_speed_val": 0,"recv_servo_speed_stats": "","recv_servo_torque_val": 0,"recv_servo_torque_stats": ""},
                "serial_servo_18": {
                    "device_id"       : 18,"servo_name"           : "right-front-tibia","time_stamp": 0,
                    "send_servo_valid": False,"send_servo_pos_val": 0,"send_servo_pos_stats": "","send_servo_speed_val": 0,"send_servo_speed_stats": "","send_servo_torque_val": 0,"send_servo_torque_stats": "",
                    "recv_servo_valid": False,"recv_servo_pos_val": 0,"recv_servo_pos_stats": "","recv_servo_speed_val": 0,"recv_servo_speed_stats": "","recv_servo_torque_val": 0,"recv_servo_torque_stats": ""}
            },
            "valve_pumps":{
            "right-middle": {"valve_pump_id": 0, "valve_pump_name": "right-middle-valpump","recv_pump_status": 1,"turn_onoff_val_pump": 2,"time_stamp": 0},
            "right-front" : {"valve_pump_id": 1, "valve_pump_name": "right-front-valpump" ,"recv_pump_status": 1,"turn_onoff_val_pump": 2,"time_stamp": 0},
            "left-front"  : {"valve_pump_id": 2, "valve_pump_name": "left-front-valpump"  ,"recv_pump_status": 1,"turn_onoff_val_pump": 2,"time_stamp": 0},
            "left-middle" : {"valve_pump_id": 3, "valve_pump_name": "left-middle-valpump" ,"recv_pump_status": 1,"turn_onoff_val_pump": 2,"time_stamp": 0},
            "left-back"   : {"valve_pump_id": 4, "valve_pump_name": "left-back-valpump"   ,"recv_pump_status": 1,"turn_onoff_val_pump": 2,"time_stamp": 0},
            "right-back"  : {"valve_pump_id": 5, "valve_pump_name": "right-back-valpump"  ,"recv_pump_status": 1,"turn_onoff_val_pump": 2,"time_stamp": 0}
            }
        }

        if cmu_msg_dic == None:
            self.cmu_msg_dic = cmu_msg_dic_tmplt
        else: 
            self.cmu_msg_dic = deepcopy(cmu_msg_dic)
    
    def print_sel_row(self,svo_row:int=None, vpump_row:int=None,elmt_head = True):
        '''
        Given svo_row or vpump_row, print out that row. 

        Param svo_row  : Value from 1--18
        Param vpump_row: Value from 0--5
        Param elmt_head: Eliminate head or not. 

        Return         : Printed string
        '''

        cmu_keys    = list(self.cmu_msg_dic.keys())

        apend_str = ""

        # For servos: 
        if(svo_row != None):
            svo_key   = cmu_keys[0]

            if elmt_head == False:
                apend_str = apend_str + "##########"+svo_key + ": \n"

            sub_key = self.ssvo_head+str(svo_row)

            name     = self.cmu_msg_dic[svo_key][sub_key]["servo_name"           ]
            send_pos = self.cmu_msg_dic[svo_key][sub_key]["send_servo_pos_val"   ]
            send_spd = self.cmu_msg_dic[svo_key][sub_key]["send_servo_speed_val" ]
            send_tq  = self.cmu_msg_dic[svo_key][sub_key]["send_servo_torque_val"]
            recv_pos = self.cmu_msg_dic[svo_key][sub_key]["recv_servo_pos_val"   ]
            recv_spd = self.cmu_msg_dic[svo_key][sub_key]["recv_servo_speed_val" ]
            recv_tq  = self.cmu_msg_dic[svo_key][sub_key]["recv_servo_torque_val"]
            t_stamp  = self.cmu_msg_dic[svo_key][sub_key]["time_stamp"           ]


            # For sub key 
            if(len(sub_key)<15):
                sub_key = sub_key +" "*(15-len(sub_key))
            apend_str = apend_str + sub_key + ":"

            # for name 
            if(len(name)<18):
                name = name +" "*(18-len(name))

            # for send pose: 
            spos = "sndpos:" + f"{send_pos:+5d},"
            sspd = "sndspd:" + f"{send_spd:+5d},"
            stq  = "sndtq:"  + f"{send_tq :+5d},"
            rpos = "rcvpos:" + f"{recv_pos:+5d},"
            rspd = "rcvspd:" + f"{recv_spd:+5d},"
            rtq  = "rcvtq:"  + f"{recv_tq :+5d},"

            t_stamp   = "t: "+ f"{t_stamp :+6.3f}"
            apend_str = apend_str + name + ":" + spos + sspd + stq + rpos+ rspd + rtq + t_stamp + " \n"

        # For vpumps: 
        vpump_key = cmu_keys[1]

        if vpump_row != None: 
            if elmt_head == False:
                apend_str = apend_str + "##########"+vpump_key + ": \n"
            sub_key = self.leg_nams[vpump_row]

            name      = sub_key
            vpump_id  = self.cmu_msg_dic[vpump_key][sub_key]["valve_pump_id"      ]
            recv_stat = self.cmu_msg_dic[vpump_key][sub_key]["recv_pump_status"   ]
            on_off    = self.cmu_msg_dic[vpump_key][sub_key]["turn_onoff_val_pump"]
            t_stamp   = self.cmu_msg_dic[vpump_key][sub_key]["time_stamp"         ]

            # for name 
            if(len(name)<13):
                name = name +" "*(13-len(name))

            vpump_id  = "vpump_id:"  +f"{vpump_id :+3d},"
            recv_stat = "recv_stat:" +f"{recv_stat:+3d},"
            on_off    = "on_off:"    +f"{on_off   :+3d},"
            t_stamp   = "t_stamp:"   +f"{t_stamp  :+3d}"
        
            apend_str = apend_str + name + ":"+vpump_id+recv_stat+ on_off+t_stamp+ " \n"

        print(apend_str)
        return(apend_str)
    
    def form_str(self):

        off_str  = '\033[0m\033[27m'
        bold_str = '\033[1m'
        blue_str = '\033[34m'
        gren_str = '\033[32m'

        cmu_keys  = list(self.cmu_msg_dic.keys())
        apend_str = ""

        # For servos: 
        svo_key   = cmu_keys[0]
        apend_str = apend_str +gren_str+bold_str+ "##########"+svo_key + ": \n"+off_str
        for sub_key in self.cmu_msg_dic[svo_key]:

            name     = self.cmu_msg_dic[svo_key][sub_key]["servo_name"           ]
            send_pos = self.cmu_msg_dic[svo_key][sub_key]["send_servo_pos_val"   ]
            send_spd = self.cmu_msg_dic[svo_key][sub_key]["send_servo_speed_val" ]
            send_tq  = self.cmu_msg_dic[svo_key][sub_key]["send_servo_torque_val"]
            recv_pos = self.cmu_msg_dic[svo_key][sub_key]["recv_servo_pos_val"   ]
            recv_spd = self.cmu_msg_dic[svo_key][sub_key]["recv_servo_speed_val" ]
            recv_tq  = self.cmu_msg_dic[svo_key][sub_key]["recv_servo_torque_val"]
            t_stamp  = self.cmu_msg_dic[svo_key][sub_key]["time_stamp"           ]


            # For sub key 
            if(len(sub_key)<15):
                sub_key = sub_key +" "*(15-len(sub_key))
            apend_str = apend_str + sub_key + ":"

            # for name 
            if(len(name)<18):
                name = name +" "*(18-len(name))

            # for send pose: 
            spos = "sndpos:" + f"{send_pos:+5d},"
            sspd = "sndspd:" + f"{send_spd:+5d},"
            stq  = "sndtq:"  + f"{send_tq :+5d},"
            rpos = "rcvpos:" + f"{recv_pos:+5d},"
            rspd = "rcvspd:" + f"{recv_spd:+5d},"
            rtq  = "rcvtq:"  + f"{recv_tq :+5d},"

            t_stamp = "t: "+ f"{t_stamp :+6.3f}"

            apend_str = apend_str + name + ":" + spos + sspd + stq + rpos+ rspd + rtq + t_stamp + " \n"

        # For vpumps: 
        vpump_key = cmu_keys[1]

        apend_str = apend_str + gren_str+bold_str+ "##########"+vpump_key + ": \n"+off_str

        for sub_key in self.cmu_msg_dic[vpump_key]:
            name      = sub_key
            vpump_id  = self.cmu_msg_dic[vpump_key][sub_key]["valve_pump_id"      ]
            recv_stat = self.cmu_msg_dic[vpump_key][sub_key]["recv_pump_status"   ]
            on_off    = self.cmu_msg_dic[vpump_key][sub_key]["turn_onoff_val_pump"]
            t_stamp   = self.cmu_msg_dic[vpump_key][sub_key]["time_stamp"         ]

            # for name 
            if(len(name)<13):
                name = name +" "*(13-len(name))

            vpump_id  = "vpump_id:"  +f"{vpump_id :+3d},"
            recv_stat = "recv_stat:" +f"{recv_stat:+3d},"
            on_off    = "on_off:"    +f"{on_off   :+3d},"
            t_stamp   = "t_stamp:"   +f"{t_stamp  :+3d}"
        
            apend_str = apend_str + name + ":"+vpump_id+recv_stat+ on_off+t_stamp+ " \n" 
        
        return(apend_str)
        
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


    def set_rcv_one_svo(self,svo_id:int,pulse_val,spd_raw ,torq_raw ):
        '''
        Given svo_id, set receive  from servo's 
            pulse position, raw torque value, and raw speed value  

        Param svo_id   : 1--18
        Param pulse_val: Pulse position 
        Param torq_raw : Torque in raw format
        Param spd_raw  : speed in pulses/sec

        return         : self.cmu_msg_dic
        '''
        svo_idx = self.ssvo_head+str(int(svo_id))

        self.cmu_msg_dic["serial_servos"][svo_idx]['recv_servo_valid'     ] = True
        self.cmu_msg_dic["serial_servos"][svo_idx]["recv_servo_torque_val"] = int(torq_raw) 
        self.cmu_msg_dic["serial_servos"][svo_idx]["recv_servo_speed_val" ] = int(spd_raw )
        self.cmu_msg_dic["serial_servos"][svo_idx]["recv_servo_pos_val"   ] = int(pulse_val)
        
    def set_recv_stat_one_svo(self,svo_id:int,pulse_sta:str="",spd_sta:str="",torq_sta:str=""):
        '''
        Given svo_id, set send to servo's status for pulse position, raw torque value, and raw speed  
        
        Param svo_id   : 1--18
        Param pulse_sta: In str  
        Param torq_sta : In str 
        Param spd_sta  : In str 

        return         : self.cmu_msg_dic
        '''
        svo_idx = self.ssvo_head+str(int(svo_id))

        self.cmu_msg_dic["serial_servos"][svo_idx]["recv_servo_torque_stats"] = pulse_sta
        self.cmu_msg_dic["serial_servos"][svo_idx]["recv_servo_speed_stats" ] = spd_sta
        self.cmu_msg_dic["serial_servos"][svo_idx]["recv_servo_pos_stats"   ] = torq_sta

        return self.cmu_msg_dic

    def set_snd_stat_one_svo(self,svo_id:int,pulse_sta:str="",spd_sta:str="",torq_sta:str=""):
        '''
        Given svo_id, set send to servo's status for pulse position, raw torque value, and raw speed  
        
        Param svo_id   : 1--18
        Param pulse_sta: In str  
        Param torq_sta : In str 
        Param spd_sta  : In str 

        return         : self.cmu_msg_dic
        '''
        svo_idx = self.ssvo_head+str(int(svo_id))

        self.cmu_msg_dic["serial_servos"][svo_idx]["send_servo_torque_stats"] = pulse_sta
        self.cmu_msg_dic["serial_servos"][svo_idx]["send_servo_speed_stats" ] = spd_sta
        self.cmu_msg_dic["serial_servos"][svo_idx]["send_servo_pos_stats"   ] = torq_sta

        return self.cmu_msg_dic
        
    def set_snd_one_svo(self,svo_id:int,pulse_val:int=0,spd_raw:int=100,torq_raw:int=100):
        '''
        Given svo_id, set send to servo's pulse position, raw torque value, and raw speed value  
        
        Param svo_id   : 1--18
        Param pulse_val: Pulse position 
        Param torq_raw : Torque in raw format
        Param spd_raw  : speed in pulses/sec
        
        return         : self.cmu_msg_dic
        '''
        svo_idx = self.ssvo_head+str(int(svo_id))

        # torq 
        self.cmu_msg_dic["serial_servos"][svo_idx]["send_servo_torque_val"] = int(torq_raw)
        self.cmu_msg_dic["serial_servos"][svo_idx]["send_servo_speed_val" ] = int(spd_raw)
        self.cmu_msg_dic["serial_servos"][svo_idx]["send_servo_pos_val"   ] = int(pulse_val)
        self.cmu_msg_dic["serial_servos"][svo_idx]['send_servo_valid'     ] = True

        return self.cmu_msg_dic

    def set_svo_tstamp(self,svo_id:int,tstamp:float):
        '''
        Given svo_id, set send to servo's pulse position, raw torque value, and raw speed value  
        
        Param svo_id   : 1--18
        return         : self.cmu_msg_dic
        '''
        
        svo_idx = self.ssvo_head+str(int(svo_id))
        self.cmu_msg_dic["serial_servos"][svo_idx]["time_stamp"] = tstamp
        
        return self.cmu_msg_dic
    
    def set_ileg_vpumps(self,ileg:int,dis_ena:bool=2):
        '''
        Set vpumps by given leg index and  dis_ena status
        param : dis_ena    : OFF_VALV = 0, ON_VALV = 1, NO_ACT_VALV = 2
        return: self.cmu_msg_dic
        '''    
        self.cmu_msg_dic["valve_pumps"][self.leg_nams[ileg]]["turn_onoff_val_pump"] = dis_ena
        return self.cmu_msg_dic

    def set_all_vpumps(self,dis_ena=2):
        '''
        Set all vpumps by given dis_ena status
        param : dis_ena: OFF_VALV = 0, ON_VALV = 1, NO_ACT_VALV = 2
        return: self.cmu_msg_dic
        '''

        for leg_nam in self.leg_nams:
            self.cmu_msg_dic["valve_pumps"][leg_nam]["turn_onoff_val_pump"] = dis_ena

        return self.cmu_msg_dic

    def get_ileg_vpumps(self,ileg:int)->bool:
        '''
        Set vpumps by given leg index and  dis_ena status
        return: dis_ena    : OFF_VALV = 0, ON_VALV = 1, NO_ACT_VALV = 2
        
        '''    
        dis_ena = self.cmu_msg_dic["valve_pumps"][self.leg_nams[ileg]]["turn_onoff_val_pump"] 
        
        return dis_ena

    def get_cmu_msg_dic(self):
        return self.cmu_msg_dic
    
    def get_rcv_one_svo(self,svo_id:int)->List[Union[int,int,int]]:
        '''
        Given svo_id, Get receive from servo's pulse position, raw torque value, and raw speed value  

        Param svo_id   : 1--18
        return         : [pulse,spd,torq,tstmp] if no valid data, return [None,None,None`]

        '''

        svo_idx = self.ssvo_head+str(int(svo_id))

        if (self.cmu_msg_dic["serial_servos"][svo_idx]['recv_servo_valid'] == True):
            torq_raw  = self.cmu_msg_dic["serial_servos"][svo_idx]["recv_servo_torque_val"]
            spd_raw   = self.cmu_msg_dic["serial_servos"][svo_idx]["recv_servo_speed_val" ] 
            pulse_val = self.cmu_msg_dic["serial_servos"][svo_idx]["recv_servo_pos_val"   ]
            tstmp     = self.cmu_msg_dic["serial_servos"][svo_idx]["recv_stamp"           ]
            return [pulse_val,spd_raw,torq_raw,tstmp]
        
        else: 
            [None,None,None,None]

    def get_snd_valid_stat(self,svo_id:int)->bool:
        """
        Get the send to servo's message valid state 

        """
        svo_idx = self.ssvo_head+str(int(svo_id))
        vad_stat = self.cmu_msg_dic["serial_servos"][svo_idx]['send_servo_valid'] 
        
        return vad_stat
    
    def get_recv_valid_stat(self,svo_id:int)->bool:
        """
        Get the receive from servo's message valid state 

        """
        svo_idx = self.ssvo_head+str(int(svo_id))
        vad_stat = self.cmu_msg_dic["serial_servos"][svo_idx]['recv_servo_valid'] 
        
        return vad_stat
    
    def get_snd_one_svo(self,svo_id:int)->List[Union[int,int,int]]:
        '''
        Given svo_id, Get send to servo's pulse position, raw torque value, and raw speed value  

        Param svo_id   : 1--18
        return         : [pulse,spd,torq,tstmp] if no valid data, return [None,None,None`]

        '''

        svo_idx  = self.ssvo_head+str(int(svo_id))

        if (self.cmu_msg_dic["serial_servos"][svo_idx]['send_servo_valid'] == True):
            torq_raw  = self.cmu_msg_dic["serial_servos"][svo_idx]["send_servo_torque_val"]
            spd_raw   = self.cmu_msg_dic["serial_servos"][svo_idx]["send_servo_speed_val" ] 
            pulse_val = self.cmu_msg_dic["serial_servos"][svo_idx]["send_servo_pos_val"   ]
            tstmp     = self.cmu_msg_dic["serial_servos"][svo_idx]["time_stamp"           ]
            return [pulse_val,spd_raw,torq_raw,tstmp]
        
        else: 
            [None,None,None,None]

    def get_num_svos(self):
        return self.num_svos
    
    def get_num_legs(self):
        return self.num_legs
    
    def get_ileg_names(self,i:int):
        """
        Given leg id (int), return string type leg name 
        """
        return self.leg_nams[i]


    def __str__(self):

        cmu_msg_str = self.form_str()
        return(cmu_msg_str)
    
def test1():
    import time
    cmu = BotCmuMsgType("cmu")
    for i in range(5):
        
        cmu.set_all_vpumps(i%2)
        cmu.set_snd_one_svo(3+i,12,13,136)
        cmu.print_table()
        #print(cmu)
        time.sleep(0.5)
        
    cmu.print_sel_row(None,1)
    #print("cmu.get_rcv_one_svo(3): "+str(cmu.get_rcv_one_svo(3)))


if __name__ == "__main__":
    test1()