#!/bin/env python
# -*- coding: utf-8 -*-
"""
Lock class

Authors: shechenglu(shechenglu@baidu.com)
Date:    2015/07/02 17:23:06
"""
import threading

class Lock(object):
    """Lock
    Singleton Wrapper of the threading.Lock
    """

    lock = None

    @staticmethod
    def retrive_lock():
        """Get the lock
        Args:
            None
        Return:
            Lock obj
        """
        if not Lock.lock:
            Lock.lock = threading.Lock()
        return Lock.lock
