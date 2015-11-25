#!/bin/env python
#-*- coding: utf8 -*-
"""
Test Page class

author: shechenglu@baidu.com
date: 2015/09/04
"""

import sys
import unittest
sys.path.append("../")

import page

class TestPage(unittest.TestCase):
    """TestPage
    """

    def test_hydrate(self):
        """testHydrate
        Args:
            None
        Return
            None
        """
        page1 = page.Page("www.baidu.com", 5)
        page1.hydrate()
        self.assertEqual(page1.charset, "utf-8")
        self.assertEqual(page1.code, 200)

    def test_get_elements_by_tag_name(self):
        """testGetElementsByTagName
        Args:
            None
        Return
            None
        """
        page2 = page.Page("www.baidu.com", 5)
        page2.hydrate()
        logo = page2.get_elements_by_tag_name("img")[0]["src"]
        self.assertEqual(logo, "//www.baidu.com/img/bd_logo1.png")

if __name__ == "__main__":
    unittest.main()
