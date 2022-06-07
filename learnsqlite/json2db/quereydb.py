import sqlite3
con = sqlite3.connect('example.db')
cur = con.cursor()
for row in cur.execute('SELECT * FROM serial_servo_commu  ORDER BY time_stamp'):
        print(row)
