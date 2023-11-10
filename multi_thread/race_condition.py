# https://superfastpython.com/thread-race-condition-shared-variable/
# SuperFastPython.com
# example of a race condition with a shared variable
from threading   import Thread
from collections import deque
import threading
import time
threadLock = threading.Lock()
value = []
vdq = deque()
#################case 1 #################
#########################################
# make additions into the global variable
def adder(amount, repeats):
    global value

    #threadLock.acquire()
    for _ in range(repeats):
        value = value+[amount]
    #threadLock.release()
 
# make subtractions from the global variable
def subtractor(amount, repeats):
    global value
    
    #threadLock.acquire()
    for _ in range(repeats):
        value = value[0:-1]
    #threadLock.release()

def case1_race_cond_lst():
    # start a thread making additions
    adder_thread = Thread(target=adder, args=(100, 10000))
    adder_thread.start()
    # start a thread making subtractions
    subtractor_thread = Thread(target=subtractor, args=(100, 10000))
    subtractor_thread.start()

    # wait for both threads to finish
    print('Waiting for threads to finish...')
    adder_thread.join()
    subtractor_thread.join()
    # report the value
    print(f'Value: {value}')
    print(len(value))

#################case 2 #################
#########################################
# make additions into the global variable
def adder2(amount, repeats):
    global value
    threadLock.acquire()
    for _ in range(repeats):
        value = value+[amount]
    threadLock.release()
 
# make subtractions from the global variable
def subtractor2(amount, repeats):
    global value
    threadLock.acquire()
    for _ in range(repeats):
        value = value[0:-1]
    threadLock.release() 
def case2_race_cond_lst_lock():
    # start a thread making additions
    adder_thread = Thread(target=adder2, args=(100, 10000))
    adder_thread.start()
    # start a thread making subtractions
    subtractor_thread = Thread(target=subtractor2, args=(100, 10000))
    subtractor_thread.start()

    # wait for both threads to finish
    print('Waiting for threads to finish...')
    adder_thread.join()
    subtractor_thread.join()
    # report the value
    print(f'Value: {value}')
    print(len(value))


#################case 3 #################
#########################################
def adder3(amount, repeats):
    global value
    for _ in range(repeats):
        vdq.append(amount)
 
# make subtractions from the global variable
def subtractor3(amount, repeats):
    global value
    for _ in range(repeats):
        if len(vdq) !=0:
            vdq.popleft()

def case3_race_cond_dequeue():
    # start a thread making additions
    adder_thread = Thread(target=adder3, args=(100, 100002))
    adder_thread.start()
    # start a thread making subtractions
    subtractor_thread = Thread(target=subtractor3, args=(100, 100000))
    subtractor_thread.start()

    # wait for both threads to finish
    print('Waiting for threads to finish...')
    adder_thread.join()
    subtractor_thread.join()
    # report the value
    #print(f'Value: {vdq}')
    print(len(vdq))

  
if __name__ == "__main__":
    #case1_race_cond_lst()
    #case2_race_cond_lst_lock()
    case3_race_cond_dequeue()

