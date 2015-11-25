#!/bin/env python
#-*- coding: utf8 -*-
"""
Test Spider class

author: shechenglu@baidu.com
date: 2015/09/04
"""
import os
import sys
import shutil
import unittest
sys.path.append("../")

import spider
import task

class TestSpider(unittest.TestCase):
    """TestSpider
    """

    def test_handle_fetch_baidu(self):
        """testHandle
        Args:
            None
        Return
            None
        """
        os.mkdir("./output")
        spider1 = spider.Spider(2, "", "./test/output", 1)
        task1 = task.Task("www.baidu.com", 2)
        spider1.handle(task1)
        result_file = os.path.join(os.path.realpath("."), "output",
                                   "http:\\\\www_baidu_com")
        self.assertTrue(os.path.isfile(result_file))
        self.assertTrue(os.path.getsize(result_file) > 0)

    def test_handle_fetch_segmentfault(self):
        """test_handle_fetch_segmentfault
        Args:
            None
        Return
            None
        """
        spider2 = spider.Spider(2, "", "./test/output", 1)
        task2 = task.Task("segmentfault.com", 2)
        spider2.handle(task2)
        result_file = os.path.join(os.path.realpath("."), "output",
                                   "http:\\\\segmentfault_com")
        self.assertTrue(os.path.isfile(result_file))
        self.assertTrue(os.path.getsize(result_file) > 0)
        shutil.rmtree("./output")


if __name__ == "__main__":
    unittest.main()
