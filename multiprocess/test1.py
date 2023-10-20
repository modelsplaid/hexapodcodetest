# reference: https://docs.python.org/3/library/multiprocessing.html
from multiprocessing import Pool
from multiprocessing import Process, Value, Array,RawArray
import multiprocessing as mp
from multiprocessing import Process, Manager
import os
import time 

def f(x):
    print(time.time())
    print(x)
    return x*x

def f1(x):
    print(time.time())
    print(x)

def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())

    while(True):
        pass 

global dic_msg
dic_msg = 1
def queue_process(q1,q2):
    
    
    for i in range(5):
        time.sleep(0.1)
        q1.put('hello q1: '+str(i))
        q2.put('hello q2: '+str(i))
        #print(q2.get(block=False))
        #print("q2.size(): "+str(q2.qsize()))

def test_pool():
    with Pool(1) as p:
        print(p.map(f, [1, 2, 3]))

def test_process():
    p = Process(target=info, args=('bob',))
    p.start()
    #p.join()
    print('main process:', os.getpid())
    #while(True):
    #    pass 

def test_spawn():
    mp.set_start_method('spawn')
    q = mp.Queue()
    p = mp.Process(target=info, args=(q,))
    p.start()
    print(q.get())
    p.join()

def test_queu():
    mp.set_start_method('forkserver')
    q1 = mp.Queue()
    q2 = mp.Queue()
    p = mp.Process(target=queue_process, args=(q1,q2))
    p.start()

    for i in range(5):
        time.sleep(0.1)
        print("q2.size(): "+str(q2.qsize())) # todo; here: why q1 always 0?
        print("q1.size(): "+str(q1.qsize())) # todo; here: why q1 always 0?


def f_share_mem(n, a):
    n.value = 3.1415927
    for i in range(len(a)):
        a[i] = str(-a[i])

def test_share_mem():
    num = Value('d', 0.0)
    #arr = Array('i', range(10))
    arr = RawArray('i', range(10))

    p = Process(target=f_share_mem, args=(num, arr))
    p.start()
    p.join()

    print(num.value)
    print(arr[:])


def fg_mana(d, l):

    for i in range(10):
        d[1] = int(i)
        d['2'] = str(i+1)
        d[0.25] = i*0.1
        l.reverse()
        time.sleep(0.1)

def test_manager():
    with Manager() as manager:
        d = manager.dict()
        l = manager.list(range(10))

        p = Process(target=fg_mana, args=(d, l))
        p.start()
        #p.join()
    for i in range(10):
        print(d)
        print(l)
        time.sleep(0.1)

if __name__ == '__main__':
    #test_process()
    #test_spawn()
    #test_queu()
    #test_share_mem()
    test_manager()


