#! /usr/bin/env python
# _*_ coding:utf-8 _*_
import time
import sys

__author__ = 'ilbsmart'

import Queue
import threading
import traceback


def _handle_thread_exc(task, exc_info):
    traceback.print_exception(*exc_info)


class Task(object):
    def __init__(self, thread_func, args=None, kwargs=None, callback=None):
        self.thread_func = thread_func
        self.args = args or []
        self.kwargs = kwargs or {}
        self.request_id = id(self)
        self.callback = callback
        self.exception = False
        self.exc_callback = _handle_thread_exc


class NoThreadsAvailable(Exception):
    pass


class ThreadPool(object):
    def __init__(self, thread_num, work_queue_num, result_queue_num):
        self.th_nu = thread_num
        self.work_queue = Queue.Queue(work_queue_num)
        self.result_queue = Queue.Queue(result_queue_num)
        self.threads = []
        self._init_thread_pool()

    def _init_thread_pool(self):
        for i in range(1, self.th_nu):
            self.threads.append(WorkThread(self.work_queue, self.result_queue))

    def add_task(self, thread_func, args=None, kwargs=None, callback=None):
        self.work_queue.put(Task(thread_func, args, kwargs, callback))

    def wait(self):
        while True:
            if not self.threads:
                raise (NoThreadsAvailable, "no threads available")
            try:
                task, result = self.result_queue.get()
                if task.exception:
                    task.exc_callback(task, result)
                elif task.callback:
                    task.callback(task, result)
            except Queue.Empty():
                break

    def fini_thread_pool(self):
        for i in self.threads:
            if i.isAlive():
                i.join()


class WorkThread(threading.Thread):
    def __init__(self, work_queue, result_queue):
        super(WorkThread, self).__init__()
        self._work_queue = work_queue
        self._result_queue = result_queue
        self.start()

    def run(self):
        while True:
            try:
                task = self._work_queue.get()
                result = task.thread_func(task.args, task.kwargs, task.callback)
                self._result_queue.put((task, result))
                self._work_queue.task_done()
            except:
                task.exception = True
                self._result_queue.put((task, sys.exc_info()))


def work_func(args, kwargs, callback):
    print "thread {} start...".format(args[0])
    time.sleep(0.1)
    return args[0]


def work_func_cb(task, result):
    print "nothing, just print the result: {}".format(result)



if __name__ == '__main__':
    print "start..."
    zem_thread_pool = ThreadPool(10, 100, 100)
    for i in range(100):
        zem_thread_pool.add_task(work_func, (i,), callback=work_func_cb)
    zem_thread_pool.wait()
    zem_thread_pool.fini_thread_pool()
    print "finish"
