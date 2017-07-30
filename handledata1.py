#-*- coding: utf-8 -*-
/**
源文件:gbk
结果文件:gbk
*/

import __init__

import sys
import os
import codecs
from sets import Set

reload(sys)
sys.setdefaultencoding('utf-8')

def processline(line, map):
	a = line.split(',')
	mobile = a[1].replace('\n','')
	pname = a[0]
	if not map.get(mobile):
		map[mobile] = Set([])
	map[mobile].add(pname)
	
def handle():
	filepath = '娱乐宝7期.csv'.encode('gbk')
	print filepath
	f = open(filepath, 'r')
	resultmap = {}
	
	for line in f:
		#print line.split(",")[1].replace('\n', '')
		processline(line, resultmap)
	
	for key in resultmap.iterkeys():
		#print key
		print '%s,%s' % ((key, ('、'.encode("gbk").join(resultmap.get(key)))))

def main():
	handle()

if __name__ == '__main__':
    main()
