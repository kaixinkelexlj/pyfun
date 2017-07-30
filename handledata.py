#-*- coding: gbk -*-
'''
@author lujun.xlj@2015-10-23
src-file-encode:gbk
'''

import sys
import os
import codecs
import re
from sets import Set

import __init__


reload(sys)
sys.setdefaultencoding('gbk')

def processline(line, map):
	a = line.split(',')
	mobile = re.sub(r'[\r\n]', '', a[1])
	pname = a[0]
	if not map.get(mobile):
		map[mobile] = Set([])
	map[mobile].add(pname)
	
def handle(path):
	filepath = path
	f = open(filepath, 'r')
	resultmap = {}
	
	for line in f:
		#print line.split(',')[1].replace('\n','')
		processline(line, resultmap)
	
	for key in resultmap.iterkeys():
		#print key
		print '%s,%s\r' % ((key, ('、'.encode("gbk").join(resultmap.get(key)))))

def srccheck(path):
	if not path:
		print '\nsrc file path is empty!!'
		return None
	if not os.path.exists(path):
		print '\nsrc file:%s not exists' % (path)
		return None
	return path
		
def main():
	if len(sys.argv) < 2:
		print 'usage:\npy %s <src-data-file-path>' % (__file__)
		sys.exit(1)
	f = srccheck(sys.argv[1])
	if not f:
		sys.exit(1)
	handle(f)

if __name__ == '__main__':
    main()
