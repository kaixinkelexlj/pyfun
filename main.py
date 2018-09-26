#!/usr/bin/python
# coding=utf-8

import requests


def http_request():
    r = requests.get("https://www.baidu.com")
    print r.text;


# http_request();

print "text[%s], url[%s]" % (1, 2)
