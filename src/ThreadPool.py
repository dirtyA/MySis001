#coding=utf-8

import threading;
import queue;
import time;
import traceback;

class ThreadPool:
    def thread_func(self):
        while(True):
            task = None;
            while(True):
                try:
                    task = self.queue.get(timeout = 2);
                    break;
                except:
                    if(self.status != "start"):
                        break;
                    continue;
            if(task == None and self.status != "start" and self.queue.empty()):
                break;
            try:
                func = task["func"];
                args = task["args"];
                func(*args);
            except Exception as e:
                print("Catch exception:");
                val = traceback.format_exc();
                print(val);
        
    def __init__(self, size):
        self.size = size;
        self.queue = queue.Queue();
        #ready, start, shutdown;
        self.status = "ready";
        self.mutex = threading.Lock();
        self.pool = [];
        for i in range(0, size):
            thr = threading.Thread(target = self.thread_func);
            self.pool.append(thr);
        
    def addTask(self, func, *args):
        ret = True;
        if(self.status == "start"):
            self.mutex.acquire();
            if(self.status == "start"):
                self.queue.put({"func":func, "args":args});
                ret = True;
            else:
                ret = False;
            self.mutex.release();
        else:
            ret = False;
        return ret;
            
    def start(self):
        ret = True;
        if(self.status == "ready"):
            self.mutex.acquire();
            if(self.status == "ready"):
                self.status = "start";
                for thr in self.pool:
                    thr.start();
                ret = True;
            else:
                ret = False;
            self.mutex.release();
        else:
            ret = False;
        return ret;
        
    def shutdown(self):
        ret = True;
        if(self.status == "start"):
            self.mutex.acquire();
            if(self.status == "start"):
                self.status = "shutdown";
                ret = True;
            else:
                ret = False;
            self.mutex.release();
            if(ret == True):
                for item in self.pool:
                    item.join();
        else:
            ret = False;
        return ret;
        
def test(a, b):
    print("a={0} b = {1} a+b={2}".format(a, b, a + b));
        
def testOne(a):
    print("Got a={0}".format(a));
    time.sleep(1);
        
def main():
    pool = ThreadPool(4);
    pool.start();
    for i in range(0, 10):
        pool.addTask(test, i, str(i + 1));
    for i in range(0, 20):
        pool.addTask(testOne, i);
    #time.sleep(5);
    pool.shutdown();
    
if(__name__ == "__main__"):
    main();