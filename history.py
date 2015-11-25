#!/bin/env python
# -*- coding: utf-8 -*-
"""
History class

Authors: shechenglu(shechenglu@baidu.com)
Date:    2015/10/25 17:23:06
"""

class History(object):
    """History
    Where to hold the history task
    """

    history = None

    @staticmethod
    def retrive_history():
        """Get history holder
        Args:
            None
        Return:
            history task list
        """
        if not History.history:
            History.history = []
        return History.history
