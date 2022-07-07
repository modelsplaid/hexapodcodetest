import sqlite3
import queue
import json
class servoCommuJson2DB: 
    def __init__(self):
        self.con = []
        self.cur = []
    def connect(self,database_file = 'example.db'):
        self.con = sqlite3.connect(database_file)
        self.cur = self.con.cursor()

    def load_servo_json_recoredr(self,json_file_name = "recorded_servo_data.json"):
        #load json file
        try:
            out_file = open(json_file_name, "r")
            data_json = json.load(out_file)   
            return data_json
        except: 
            print("unable load json file, try using ijson")  
            servo_queue = queue.Queue() 
            import ijson
            with open(json_file_name, "r") as f:
                for record in ijson.items(f,"item"):
                    one_frame = record
                    servo_queue.put(one_frame) 

            num_frams = servo_queue.qsize()
            data_json = []*num_frams
            for i in range(num_frams):
                data_json = servo_queue.get()
            return data_json

    def conver_json_2_db(self,json_file= "recorded_servo_data.json",db_file = 'example.db'):
        
        self.connect(db_file)
        try:
            self.execute_create_table()
        except:
            print("table already exit,insert to present db")

        jsondata = self.load_servo_json_recoredr(json_file)
        num_frams = len(jsondata)
        for i in range(num_frams):
            devs_data = jsondata[i]
            num_devs = len(devs_data)
            keyvalpair=list(devs_data.items())

            for j in range(num_devs):
                one_dev_data = keyvalpair[j][1] # get the value
                #print("one_dev_data:"+str(one_dev_data) )
                self.execute_insert_into(one_dev_data)
                
    def execute_create_table(self):
        # Create table
        self.cur.execute('''CREATE TABLE serial_servo_commu
                       (device_id integer, 
                       send_servo_valid integer, 
                       send_servo_pos_val integer,
                       send_servo_pos_stats text, 
                       send_servo_speed_val integer,
                       send_servo_speed_stats text,
                       send_servo_torque_val integer,
                       send_servo_torque_stats text,
                       recv_servo_valid integer,
                       recv_servo_pos_val integer,
                       recv_servo_pos_stats text,
                       recv_servo_speed_val integer,
                       recv_servo_speed_stats text,
                       recv_servo_torque_val integer,
                       recv_servo_torque_stats text,
                       time_stamp real               
                       )''')
    
    def jsonbool2dbint(self,json_bool):
        if(json_bool==True):
            return str(1)
        else:
            return str(0)
        

    def execute_insert_into(self,one_json_data):
        # Insert a row of data
        str_device_id = str(one_json_data["device_id"])
        str_send_servo_valid = self.jsonbool2dbint(str(one_json_data["send_servo_valid"]))
        str_send_servo_pos_val = str(one_json_data["send_servo_pos_val"])        
        str_send_servo_pos_stats = "'"+ one_json_data["send_servo_pos_stats"]+"'"
        str_send_servo_speed_val = str(one_json_data["send_servo_speed_val"])
        str_send_servo_speed_stats = "'"+one_json_data["send_servo_speed_stats"]+"'"
        str_send_servo_torque_val = str(one_json_data["send_servo_torque_val"])
        str_send_servo_torque_stats = "'"+one_json_data["send_servo_torque_stats"]+"'"
        str_recv_servo_valid = self.jsonbool2dbint(str(one_json_data["recv_servo_valid"]))
        str_recv_servo_pos_val = str(one_json_data["recv_servo_pos_val"])
        str_recv_servo_pos_stats = "'"+one_json_data["recv_servo_pos_stats"]+"'"
        str_recv_servo_speed_val = str(one_json_data["recv_servo_speed_val"])
        str_recv_servo_speed_stats = "'"+one_json_data["recv_servo_speed_stats"]+"'"
        str_recv_servo_torque_val = str(one_json_data["recv_servo_torque_val"])
        str_recv_servo_torque_stats = "'"+one_json_data["recv_servo_torque_stats"]+"'"
        str_time_stamp = str(one_json_data["time_stamp"])


        #self.cur.execute("INSERT INTO serial_servo_commu VALUES ("+str_device_id+ ",1,1200,'good',200,'good',500,'good',1,1200,'good',200,'good',500,'good',12.3)")
        
        print("INSERT INTO serial_servo_commu VALUES ("+
            str_device_id+","+
            str_send_servo_valid+","+
            str_send_servo_pos_val+","+
            str_send_servo_pos_stats+","+
            str_send_servo_speed_val+","+
            str_send_servo_speed_stats+","+
            str_send_servo_torque_val+","+
            str_send_servo_torque_stats+","+
            str_recv_servo_valid+","+
            str_recv_servo_pos_val+","+
            str_recv_servo_pos_stats+","+
            str_recv_servo_speed_val+","+
            str_recv_servo_speed_stats+","+
            str_recv_servo_torque_val+","+
            str_recv_servo_torque_stats+","+
            str_time_stamp+")")

        self.cur.execute("INSERT INTO serial_servo_commu VALUES ("+
            str_device_id+","+
            str_send_servo_valid+","+
            str_send_servo_pos_val+","+
            str_send_servo_pos_stats+","+
            str_send_servo_speed_val+","+
            str_send_servo_speed_stats+","+
            str_send_servo_torque_val+","+
            str_send_servo_torque_stats+","+
            str_recv_servo_valid+","+
            str_recv_servo_pos_val+","+
            str_recv_servo_pos_stats+","+
            str_recv_servo_speed_val+","+
            str_recv_servo_speed_stats+","+
            str_recv_servo_torque_val+","+
            str_recv_servo_torque_stats+","+
            str_time_stamp+")"
            )
    
    def commit(self):
        self.con.commit()
    
    def close(self):        
        self.con.close()

if __name__ == "__main__":
    databasefile = 'example.db'
    jsonfile = "recorded_servo_data.json"
    json2db = servoCommuJson2DB()
    json2db.conver_json_2_db()
    #json2db.connect(databasefile)
    #json2db.execute_insert_into()
    json2db.commit()
    json2db.close()
