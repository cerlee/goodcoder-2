#!/bin/env python
# -*- encoding: utf8 -*-
"""
Task wrapper

author: shechenglu@baidu.com
date: 2015/09/04
"""


class Task(object):
    """Task class
    Wrapper of the url to be fetched
    """

    def __init__(self, url, depth=0):
        """Constructor
        Args:
            url     Url
            depth   Depth of the url
        """
        self.url = url.strip()
        self.depth = depth
