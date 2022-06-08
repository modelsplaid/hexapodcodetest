import sqlite3

class servoCommuJson2DB: 
    def __init__(self):
        self.con = []
        self.cur = []
    def connect(self,database_file = 'example.db'):
        self.con = sqlite3.connect(database_file)
        self.cur = self.con.cursor()
    def load_servo_json_recoredr(self):
        #todo here
        a = 0

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
    
    def execute_insert_into(self,one_json_data = 0):
        # Insert a row of data
        device_id = 7

        self.cur.execute("INSERT INTO serial_servo_commu VALUES ("+
            str(device_id)+ ",1,1200,'good',200,'good',500,'good',1,1200,'good',200,'good',500,'good',12.3)")
    
    def commit(self):
        self.con.commit()
    
    def close(self):        
        self.con.close()

if __name__ == "__main__":
    databasefile = 'example.db'
    json2db = servoCommuJson2DB()
    json2db.connect(databasefile)
    json2db.execute_insert_into()
    json2db.commit()
    json2db.close()