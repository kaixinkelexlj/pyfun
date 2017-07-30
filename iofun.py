#!/usr/bin/env python
#-*- coding: utf8 -*-
# vim: et sw=4 ts=4
# 
###############################
#                             #
#        读取输入的工具       #
#                             # 
###############################

import sys
import re

class perline:
    """
    每行一个
    """

    @staticmethod
    def readint():
        """
        每行一个int
        """
        lines = sys.stdin.readlines()
        return map(lambda x: int(x), filter(lambda x: len(x.strip()), lines))

    @staticmethod
    def readlong():
        """
        每行一个long
        """
        lines = sys.stdin.readlines()
        return map(lambda x: long(x), filter(lambda x: len(x.strip()), lines))

    @staticmethod
    def readstr():
        """
        每行一个str
        """
        lines = sys.stdin.readlines()
        return filter(lambda x: len(x.strip()), lines)

class multiperline:
    """
    每行多个
    """

    @staticmethod
    def readstr():
        """
        每行多个
        """
        lines = sys.stdin.readlines()
        space = re.compile('\\s+')
        return map(lambda x: space.split(x.strip()), filter(lambda x: len(x.strip()), lines))

    @staticmethod
    def readint():
        """
        每行多个
        """
        lines = sys.stdin.readlines()
        space = re.compile('\\s+')
        return map(lambda x: map(lambda x: int(x), space.split(x.strip())), filter(lambda x: len(x.strip()), lines))


class csv:
    """
    每行多个
    """

    @staticmethod
    def readstr():
        """
        每行多个
        """
        lines = sys.stdin.readlines()
        space = re.compile(',')
        return map(lambda x: space.split(x.strip().strip('"')), filter(lambda x: len(x.strip()), lines))


# 可读取本地log文件 方便本地开发
# @author taomk
class reader:

    """
    读取文件 对每行进行左右边空格去除 并过滤掉空字符串 返回字符串列表
    """
    @staticmethod
    def readFile(path):

        f = open(path)
        lines = f.readlines()
        return filter(lambda x: len(x.strip()), lines)

if __name__ == '__main__':
    for line in reader.readFile('D:\log.log'):
        print line



