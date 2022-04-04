import threading, queue

q = queue.Queue()
usrdata = []
def worker():
    global usrdata
    while True:
        item = q.get()
        usrdata = usrdata +[1.23]
        print(f'Working on {item}')
        print(f'Finished {item}')
        #q.task_done()

# Turn-on the worker thread.
threading.Thread(target=worker, daemon=True).start()

# Send thirty task requests to the worker.
while True:    
    q.put(1.23)
    usrdata = usrdata[1:]

# Block until all tasks are done.
q.join()
print('All work completed')
