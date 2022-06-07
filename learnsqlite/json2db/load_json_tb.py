import sqlite3
con = sqlite3.connect('example.db')
cur = con.cursor()

# Create table
cur.execute('''CREATE TABLE serial_servo_commu
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

# Insert a row of data
cur.execute("INSERT INTO serial_servo_commu VALUES (1,1,1200,'good',200,'good',500,'good',1,1200,'good',200,'good',500,'good',12.3)")
con.commit()
con.close()