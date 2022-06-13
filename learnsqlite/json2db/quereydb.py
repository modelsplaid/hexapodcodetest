import sqlite3
con = sqlite3.connect('example.db')
cur = con.cursor()
cursor = cur.execute('SELECT * FROM serial_servo_commu  ORDER BY time_stamp')

print(type(cursor))

'''
for row in cursor:
        print(row)
'''
#https://www.tutorialspoint.com/sqlite/sqlite_python.htm