import json 
import copy
import time

out_file = open("const_hardware_config.json", "r") 
out_file2 = open("simple_servo_io_commu.json", "r") 

t1 = time.time()

config_json = json.load(out_file)
t2 = time.time()
config_json2 = json.load(out_file2)
t3 = time.time()

print("t2-t1: "+str(t2-t1) )
print("t3-t2: "+str(t3-t2) )
print("speed up(%): "+str((t3-t2-t2+t1)*100/(t3-t2)) )