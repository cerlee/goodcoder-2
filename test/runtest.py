#!/bin/env python
#-*- coding: utf8 -*-
"""
Run all test suit

author: shechenglu@baidu.com
date: 2015/09/04
"""
import unittest
import sys
import os

suits = unittest.TestLoader().discover(".", "*_test.py")
test_runner = unittest.runner.TextTestRunner()
test_runner.run(suits)
