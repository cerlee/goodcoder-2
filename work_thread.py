#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Work threads

Authors: shechenglu(shechenglu@baidu.com)
Date:    2015/07/02 17:23:06
"""
import time
import signal
import logging
import urllib2
import threading
import Queue

import spider
import taskqueue

class WorkThread(threading.Thread):
    """Work Thread
    """

    def __init__(self, spider):
        """Constructor 
        Args:
            spider Spider instance
        Return:
            None
        """
        threading.Thread.__init__(self)
        self.__exit = False
        self.__spider = spider
        self.__task_queue = taskqueue.TaskQueue.retrive_queue()

    def run(self):
        """Main function
        Args:
            None
        Return:
            None
        """
        while True:
            if self.__exit == True:
                logging.info("Thread exit method has been called, quit")
                break
            try:
                entity = self.__task_queue.get(True, 5)
                priority = entity[0]
                task = entity[1]
            except Queue.Empty:
                logging.debug("No more task to get, quit")
                self.exit()
                continue

            try:
                logging.debug("Get task {task} priority {priority}"
                                   .format(task=task.url, priority=priority))
                self.__spider.handle(task)
            except spider.SpiderException as e:
                logging.error("Error occured while processing {url}: {error}"
                                  .format(url=task.url, error=str(e)))

    def exit(self):
        """Quit
        Args:
            None
        Return:
            None
        """
        signal.alarm(1)
        self.__exit = True
