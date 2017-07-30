#-*- coding: utf-8 -*-

import __init__

import sys
import os
import codecs
from sets import Set

reload(sys)
sys.setdefaultencoding('utf-8')

def testcodecs():
	filepath = r'iotestgbk.txt'
	if os.path.exists(filepath):
		os.remove(filepath)
	f = codecs.open(filepath, 'w+', 'gbk')
	f.write('hello world\n')
	s = 'hello xlj，徐禄军\n'.encode('gbk')
	f.write(s)
	f.close()
	f = open(filepath)
	for line in f.readlines():
		print line.decode("utf-8")
	f.close()

def testR():
	pass

def testRW():
	filepath = r'iotest.txt'
	#print filepath

	if os.path.exists(filepath):
		os.remove(filepath)
	f = open(filepath, 'w+')
	f.write('hello world\n')
	f.write('hello xlj，徐禄军\n')
	f.close()
	f = open(filepath)
	for line in f.readlines():
		print line
	f.close()

def processline(line, map):
	a = line.split(',')
	mobile = a[1].replace('\n','')
	pname = a[0]
	if not map.get(mobile):
		map[mobile] = Set([])
	map[mobile].add(pname)
	
def test():
	filepath = '娱乐宝7期.csv'.encode('gbk')
	print filepath
	f = open(filepath, 'r')
	resultmap = {}
	
	for line in f:
		#print line.split(",")[1].replace('\n', '')
		processline(line, resultmap)
	
	for key in resultmap.iterkeys():
		#print key
		print '%s#%s' % ((key, (','.join(resultmap.get(key)))))

def main():
	test()

if __name__ == '__main__':
    main()
