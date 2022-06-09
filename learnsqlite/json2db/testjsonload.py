import json
import queue
out_file = open("servo_commu.json", "r") 
data_json = json.load(out_file)
dataqueue = queue.Queue()
dataqueue.put(data_json) 
dataqueue.put(data_json) 
dataqueue.put(data_json) 
dataqueue.put(data_json)
qsz=dataqueu.qsize()
json.dump(dataqueue,"jsonqueu.json")
# todo: save json queue to file according:  https://www.delftstack.com/howto/python/how-to-create-a-list-with-a-specific-size-in-python/
