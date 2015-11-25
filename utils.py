#!/bin/env python
#-*- coding: utf8 -*-
"""
Utils

author: shechenglu@baidu.com
date: 2015/09/04
"""
import os
import sys

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))

def realpath(path):
    """Convert relative path to absolute path
    Args:
        path    Absolute or relative path of a file
    Return:
        string  Absolute path of the file
    """
    if path[0] == "/":
        return path
    else:
        return os.path.join(ROOT_PATH, path)


def url2path(url):
    """Change url to a valid file name of *nix
    Args:
        url     Url
    Return:
        string  Valid file name
    """
    return url.replace("/", "\\").replace(".", "_")
