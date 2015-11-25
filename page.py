#!/bin/env python
#-*- coding: utf8 -*-
"""
Page class

author: shechenglu@baidu.com
date: 2015/09/04
"""

import re
import urllib2
import urlparse

import bs4

class Page(object):
    """Page
    A page stands up for a web page, through which to access
    response header, response body, response code and even 
    html dom tree etc..
    """

    def __init__(self, url, timeout):
        """Constructor
        Constructor will only create a empty page obj,
        call hydrate to 

        Args:
            url     Url of the page
            timeout Time of waiting for loading the page
        Return:
            None
        """
        self.timeout = timeout
        if not re.match("^http[s]{0,1}://", url):
            self.url = "http://" + url
        else:
            self.url = url

    def hydrate(self):
        """Hydrate this page
        This method will do the actual request and hydrate
        this page obj

        Args:
            None
        Return:
            None
        """
        # hydrate this page, page object
        # presents as a real page now
        self.request  = urllib2.urlopen(self.url, timeout=self.timeout)
        self.body = self.request.read()
        self.headers = self.request.info().dict
        self.realurl = self.request.geturl()
        self.code = self.request.getcode()

        components = urlparse.urlparse(self.url)
        self.protocol = components.scheme
        self.host = components.netloc
        self.path = components.path
        self.query = components.query

        # handle character setting by content-type in
        # headers or charset= from html meta tag 
        if "content-type" in self.headers:
            content_type = self.request.info().dict["content-type"]
            charset = re.findall("charset=(.*)", content_type)
            if charset:
                self.charset = charset[0]
            else:
                self.charset = "utf-8"

        if self.charset != "utf-8":
            try:
                self.body = self.body.decode(self.charset).encode("utf-8")
            except UnicodeDecodeError as e:
                raise Exception("Decode from {charset} failed: {error}"
                                .format(charset=self.charset, error=str(e)))

        self.soup = bs4.BeautifulSoup(self.body, "html.parser")
        self.encodedUrl = urllib2.quote(self.url)

    def get_elements_by_tag_name(self, tagname):
        """Get Elements By Tag Name
        Exactly the same as what it is in Javascript

        Args:
            tagname Html tag name, div, a, img etc..
        Return:
            list    A tag list
        """
        return self.soup.findAll(tagname)

    def parse_loaction_href(self):
        """Get the value of Loaction.href in the http body
        Args:
            None
        Return:
            None
        """
        return re.findall("location.href=['|\"](.*?)['|\"]", self.body)

    def get_resource_url(self, suffix):
        """Get resource url by suffix
        """
        reg = "[a-zA-Z0-9_-]*?\.(?:{suffix})".format(suffix=suffix)
        return re.findall(reg, self.body)
