import ijson
import queue
servo_queue = queue.Queue()
one_frame = []
with open("/home/pi/HexaClean/hexa_servo_analyzer/recordfiles/recorded_servo_data.json", "r") as f:
    for record in ijson.items(f,"item"):
        one_frame = record
        servo_queue.put(one_frame) 
print(one_frame["serial_servo_18"]["time_stamp"])
print(one_frame["serial_servo_18"])
    
