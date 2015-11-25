#!/bin/env python
#-*- coding: utf8 -*-
"""
Webpage Mini Spider

author: shechenglu@baidu.com
date: 2015/09/04
"""
import os
import re
import sys
import time
import signal
import logging
import argparse
import ConfigParser

import log
import task
import utils
import spider
import taskqueue
import work_thread
import thread_manager

def get_proc_version():
    """Get version of the process
    """
    return "1.0"


def get_proc_name():
    """Get name of the process
    """
    return "MiniSpider"


def h_signal(signum, frame):
    """Signal handler
    Args:
        signum  Signal number
        frame   Frame objects
    Return:
        None
    """
    logging.info("Catch signal {signal}, quit"
                 .format(signal=str(signum)))
    thread_manager.stop()
    thread_manager.join()


def add_seed_tasks(url_seeds_file):
    """Add the 0 depth urls to the task queue
    Args:
        None
    Return:
        None
    """
    if not os.path.isfile(utils.realpath(url_seeds_file)):
        logging.error("Invalid seeds file, quit")
        sys.exit(1)
    with open(url_seeds_file, "r") as seeds_file:
        for url in seeds_file:
            fetch_task = task.Task(url, 0)
            taskqueue.TaskQueue.retrive_queue().put((0, fetch_task), True, 10)


def main():
    """Main function of the process
    Args:
        None
    Return:
        None
    """
    parser = argparse.ArgumentParser(description="MiniSpider Options")
    parser.add_argument("-v", action="store_true", dest="version",
                       help="show current version and exit")
    parser.add_argument("-c", dest="conf",
                       help="path of the config file")

    args = parser.parse_args()

    if args.version:
        print "{name} v{version}".format(name=get_proc_name(), version=get_proc_version())
        sys.exit(0)

    log.init_log("./log/mini_spider")
    formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")

    if not (args.conf and os.path.isfile(args.conf)):
        logging.critical("invalid config file")
        sys.exit(1)

    config = ConfigParser.ConfigParser()
    config.read(args.conf)

    try:
        url_seeds_file = config.get("spider", "url_list_file")
        output_dir = config.get("spider", "output_directory")
        craw_timeout = config.get("spider", "crawl_timeout")
        url_pattern = config.get("spider", "target_url")
        crawl_depth = config.getint("spider", "max_depth")
        thread_num = config.getint("spider", "thread_count")
        crawl_inter = config.getfloat("spider", "crawl_interval")
    except ConfigParser.Error as e:
        logging.critical("Read config error: {error}".format(error=str(e)))
        exit(1)

    work_thread_manager = thread_manager.ThreadManager()

    signal.signal(signal.SIGTERM, h_signal)
    signal.signal(signal.SIGINT, h_signal)

    add_seed_tasks(url_seeds_file)

    worker_spider = spider.Spider(crawl_depth, url_pattern, output_dir, crawl_inter)

    for threanum in range(thread_num):
        worker_thread = work_thread.WorkThread(worker_spider)
        work_thread_manager.append_thread(worker_thread)

    work_thread_manager.start()

    # pause the main thread to receive signals
    signal.pause()


if __name__ == "__main__":
    main()
