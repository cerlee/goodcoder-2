#!/bin/env python
#-*- coding: utf8 -*-
"""
Test TaskQueue class

author: shechenglu@baidu.com
date: 2015/09/04
"""
import sys
import unittest
sys.path.append("../")

import taskqueue

class TestTaskQueue(unittest.TestCase):
    """TestTaskQueue
    """

    def test_put_normal(self):
        """testPutGet
        Args:
            None
        Return
            None
        """
        queue = taskqueue.TaskQueue.retrive_queue()
        queue.put((1, 'data1'), True, 10)

        self.assertEqual(queue.get()[1], "data1")

    def test_put_priority(self):
        """testPutGet
        Args:
            None
        Return
            None
        """
        queue = taskqueue.TaskQueue.retrive_queue()
        queue.put((3, 'data3'), True, 10)
        queue.put((1, 'data1'), True, 10)
        queue.put((4, 'data4'), True, 10)
        queue.put((2, 'data2'), True, 10)

        self.assertEqual(queue.get()[1], "data1")
        self.assertEqual(queue.get()[1], "data2")
        self.assertEqual(queue.get()[1], "data3")
        self.assertEqual(queue.get()[1], "data4")


if __name__ == "__main__":
    unittest.main()
