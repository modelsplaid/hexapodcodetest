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
        out_file = open(json_file_name, "r")
        data_json = json.load(out_file)   
        return data_json

    def conver_json_2_db(self,json_file= "recorded_servo_data.json",db_file = 'example.db'):
        self.connect(db_file)
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
                return

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
    
    def execute_insert_into(self,one_json_data):
        # Insert a row of data
        str_device_id = str(one_json_data["device_id"])
        str_send_servo_valid = str(one_json_data["send_servo_valid"])# todo here
        str_send_servo_pos_val = str(one_json_data["send_servo_pos_val"])
        
        str_send_servo_pos_stats = str(one_json_data["send_servo_pos_stats"]) # todo here

        str_send_servo_speed_val = str(one_json_data["send_servo_speed_val"])
        str_send_servo_speed_stats = str(one_json_data["send_servo_speed_stats"]) # todo here
        str_send_servo_torque_val = str(one_json_data["send_servo_torque_val"])
        str_send_servo_torque_stats = str(one_json_data["send_servo_torque_stats"])# todo here
        str_recv_servo_valid = str(one_json_data["recv_servo_valid"])# todo here
        str_recv_servo_pos_val = str(one_json_data["recv_servo_pos_val"])
        str_recv_servo_pos_stats = str(one_json_data["recv_servo_pos_stats"])# todo here
        str_recv_servo_speed_val = str(one_json_data["recv_servo_speed_val"])
        str_recv_servo_speed_stats = str(one_json_data["recv_servo_speed_stats"])# todo here
        str_recv_servo_torque_val = str(one_json_data["recv_servo_torque_val"])
        str_recv_servo_torque_stats = str(one_json_data["recv_servo_torque_stats"])# todo here
        str_time_stamp = str(one_json_data["time_stamp"])

        device_id = 7

        self.cur.execute("INSERT INTO serial_servo_commu VALUES ("+
            str(device_id)+ ",1,1200,'good',200,'good',500,'good',1,1200,'good',200,'good',500,'good',12.3)")
    
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
