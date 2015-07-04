#! /usr/bin/env python
# _*_ coding:utf-8 _*_
import time

__author__ = 'ilbsmart'


# import threading
#
# def thread_func(num):
#     print "hello, this thread name is {}".format(threading.currentThread().name)
#
#
#     print "the thread {} is ended".format(threading.currentThread().name)
#
#
# def create_threads(n):
#
#     for i in range(1, n):
#         t = threading.Thread()
#         threads.append(t)
#
#
# def start_threads():
#     for i in threads:
#         i.start()
#
#
# def main():
#     print "this thread name is {}".format(threading.currentThread().name)
#
#     create_threads(10)
#     start_threads()
#
#     for i in threads:
#         i.join()
#
# if __name__ == '__main__':
#     threads = []
#     main()

import Queue
import threading

class MyThreadPool(object):
    def __init__(self, thread_num, work_queue_num):
        self.th_nu = thread_num
        self.work_queue = Queue.Queue(work_queue_num)
        self.threads = []
        self._create_threads()
        for i in range(100):
            self.add_task(just_print, (i, ))

    def _create_threads(self):
        for i in range(self.th_nu):
            self.threads.append(WorkThread(self.work_queue))

    def add_task(self, thread_func, args):
        self.work_queue.put((thread_func, tuple(args)))


    def destroy(self):
        for i in self.threads:
            if i.isAlive():
                i.join()

class WorkThread(threading.Thread):
    def __init__(self, work_queue):
        super(WorkThread, self).__init__()
        self.work_queue = work_queue
        self.start()

    def run(self):
        while True:
            try:
                (thread_func, args) = self.work_queue.get()
                thread_func(args)
                self.work_queue.task_done()
            except Exception:
                break

def just_print(args):
    print "Helo"
    print "thread {}, print start...".format(args[0])
    time.sleep(0.1)

def print_name(name):
    time.sleep(0.1)
    print "the name is!!!!!!!!!!!!!!!!!!!!!!!!!! {}".format(name)

if __name__ == '__main__':
    print "start..."
    zem_thread_pool = MyThreadPool(10, 100)
    name = 'Grady Wong'
    zem_thread_pool.add_task(print_name, name)
    zem_thread_pool.destroy()
    print "finish"





