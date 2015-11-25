#!/bin/env python
#-*- coding: utf8 -*-
"""
Test utils class

author: shechenglu@baidu.com
date: 2015/09/04
"""

import sys
import os
import unittest
sys.path.append("../")

import utils

class TestUtils(unittest.TestCase):
    """TestUtils
    """

    def test_real_path_relative(self):
        """test relative path
        Args:
            None
        Return
            None
        """
        root = os.path.dirname(os.path.realpath("."))
        test_path1 = "./test/relative/path"
        test_path2 = "test/relative/path"

        result1 = utils.realpath(test_path1)
        result2 = utils.realpath(test_path2)

        self.assertEqual(result1, os.path.join(root, test_path1))
        self.assertEqual(result2, os.path.join(root, test_path2))

    def test_real_path_absolute(self):
        """test absolute path
        Args:
            None
        Return
            None
        """
        root = os.path.dirname(os.path.realpath("."))
        test_path = "/home/users/shechenglu/test/absolute/path"
        result3 = utils.realpath(test_path)
        self.assertEqual(result3, "/home/users/shechenglu/test/absolute/path")

    def test_url2path(self):
        """test Url2path
        Args:
            None
        Return
            None
        """
        testUrl1 = "http://baidu.com/1_2"
        result1 = utils.url2path(testUrl1)
        self.assertEqual(result1, "http:\\\\baidu_com\\1_2")

if __name__ == "__main__":
    unittest.main()
