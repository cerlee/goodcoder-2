#!/bin/env python
#-*- coding: utf8 -*-
"""
Webpage Mini Spider

author: shechenglu@baidu.com
date: 2015/09/04
"""
import signal

class ThreadManager(object):
    """ThreadManager
    Operate threads
    """

    def __init__(self):
        """Constructor
        Args:
            None
        Return:
            None
        """
        self.__stopped  = False
        self.__threads = []

    def append_thread(self, thread):
        """Add thread to ThreadManager
        Args:
            thread  Thread object
        Return:
            None
        """
        self.__threads.append(thread)

    def start(self):
        """Start all thread
        Args:
            None
        Return:
            None
        """
        for thread in self.__threads:
            thread.start()

    def stop(self):
        """Stop all thread
        Args:
            None
        Return:
            None
        """
        if self.__stopped == True:
            return
        self.__stopped = True
        for thread in self.__threads:
            thread.exit()
        for thread in self.__threads:
            thread.join()

