import json
import queue
out_file = open("servo_commu.json", "r") 
data_json = json.load(out_file)
dataqueue = queue.Queue()
dataqueue.put(data_json) 
dataqueue.put(data_json) 
dataqueue.put(data_json) 
dataqueue.put(data_json)
qsz=dataqueue.qsize()
datalist = [None]*qsz
for i in range(qsz):
    datalist[i]=dataqueue.get()

out_file = open("recorded_servo_data.json", "w")
json.dump(datalist,out_file,indent=4)
# todo: save json queue to file according:  https://www.delftstack.com/howto/python/how-to-create-a-list-with-a-specific-size-in-python/
