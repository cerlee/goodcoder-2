#!/bin/env python
# -*- coding: utf-8 -*-
"""
TaskQueue class

Authors: shechenglu(shechenglu@baidu.com)
Date:    2015/07/02 17:23:06
"""
import Queue

TASKQUEUE_MAX = 10000

class TaskQueue(object):
    """TaskQueue
    Singleton Wrapper of the PriorityQueue
    """

    queue = None

    @staticmethod
    def retrive_queue():
        """Get the queue
        Args:
            None
        Return:
            PriorityQueue
        """
        if not TaskQueue.queue:
            TaskQueue.queue = Queue.PriorityQueue(TASKQUEUE_MAX)
        return TaskQueue.queue
