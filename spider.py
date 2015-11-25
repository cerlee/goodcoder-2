#!/bin/env python
#-*- coding: utf8 -*-
"""
Spider class

author: shechenglu@baidu.com
date: 2015/09/04
"""
import os
import re
import time
import logging
import urllib2
import urlparse
import threading

import lock
import page
import task
import utils
import history
import taskqueue

class Spider(object):
    """Spider Class
    Crawl web pages and retrive useful data,
    spider got urls from a taskqueue, fetch it,
    then spawn more tasks(depends on the depth config)
    and retrive the interested data and save it 
    to local file
    """

    def __init__(self, max_dep, pattern, output_dir, frequency):
        """Constructor
        Args:
            max_dep     Depth of pages to access
            pattern     Reg pattern of the interested data
            output_dir  Directory to save the data
            frequency   Frequency of the webpage fetching
        """
        self.__max_dep = max_dep
        self.__pattern = pattern
        self.__output_dir = output_dir
        self.__task_queue = taskqueue.TaskQueue.retrive_queue()
        self.__frequency = frequency
        self.__history = history.History.retrive_history()
        self.__image_suffix = "jpg|jepg|png|gif"

    def handle(self, task):
        """Fetching routine
        Args:
            task    Task object
        Return:
            None
        """
        history_lock = lock.Lock.retrive_lock()
        history_lock.acquire()
        if task.url in self.__history:
            logging.info("Url has been fetched: {url}".format(url=task.url))
            history_lock.release()
            return
        self.__history.append(task.url)
        history_lock.release()

        if task.depth > self.__max_dep:
            raise SpiderException("Not a valid task: {task}".format(task=str(task)))

        time.sleep(self.__frequency)
        fetched_page = page.Page(task.url, 5)
        try:
            fetched_page.hydrate()
        except urllib2.HTTPError as e:
            logging.error("HTTP ERROR {url}: {error}"
                          .format(url=task.url, error=str(e)))
            return
        except urllib2.URLError as e:
            logging.error("Url ERROR {url}: {error}"
                               .format(url=task.url, error=str(e)))
            return

        if task.depth < self.__max_dep:
            self.__add_task(fetched_page, task.depth)

        imgs = fetched_page.get_resource_url(self.__image_suffix)
        if len(imgs) == 0:
            return
        path = os.path.join(utils.realpath(self.__output_dir), 
                            utils.url2path(fetched_page.url))
        try:
            if not os.path.isfile(path):
                output_file = open(path, "w")
            else:
                output_file = open(path, "a")
        except IOError as e:
            logging.error("Can't open file {path}: {error}"
                          .format(path=path, error=e[1]))
            return
        for img in imgs:
            url = self.__fix_up_url(img, fetched_page)
            output_file.write(url + "\n")
        output_file.close()

    def __add_task(self, page, depth):
        """Add task to taskQueue
        Args:
            page    Page object
            depth   Current depth of the page
        Return:
            None
        """
        urls = []
        depth = depth + 1

        urls = urls + [atag["href"] for atag in page.get_elements_by_tag_name("a")]
        urls = urls + [link["href"] for link in page.get_elements_by_tag_name("link")]
        urls = urls + [script["src"] for script in page.get_elements_by_tag_name("script")]

        urls = urls + page.parse_loaction_href()

        for url in urls:
            url = self.__fix_up_url(url, page)
            if not self.__is_valid_url(url):
                logging.info("Invalid url: {url}".format(url=url))
                continue
            fetch_task = task.Task(url, depth)
            self.__task_queue.put((depth, fetch_task), True, 10)

    def __is_valid_url(self, url):
        """Determine if a url is valid
        Args:
            url     Url
        Return:
            bool    True if url is valid else False
        """
        url_pattern = "^https?://([\da-z\.-]+)\.([\da-z\.-]+)[^ ]*$"
        js_pattern = ".*javascript\:.*"
        if re.match(url_pattern, url) and not re.match(js_pattern, url):
            return True
        else:
            return False

    def __fix_up_url(self, url, page):
        """Fix a from a web page
        A url in the web page source code is usually imcomplete,
        and the browser has some rules to complete these urls.
        This function is to act like the rules of browser.

        Args:
            url     Url
            page    Page object
        Return:
            string  A complete url
        """
        url = list(urlparse.urlparse(url.strip()))
        url[1] = page.host if url[1] == "" else url[1]
        url[0] = page.protocol if url[0] == "" else url[0]
        return urlparse.urlunparse(tuple(url))


class SpiderException(Exception):
    """SpiderException
    """

    def __init__(self, message):
        """Constructor
        Args:
            message string exception info
        Return:
            None
        """
        Exception.__init__(self, message)
