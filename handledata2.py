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

from datetime import *
import time

import __init__


reload(sys)
sys.setdefaultencoding('gbk')

def processline(line):
	parts = line.split("|")
	timestamp = long(parts[1])
	dt = time.localtime(timestamp/1000)
	s = time.strftime('%Y-%m-%d %H:%M:%S',dt)
	return   s+"##"+(",".join(parts))
	
def handle(line):
	print processline(line)
		
def main():
	if len(sys.argv) < 2:
		print 'usage:\npy %s <src-data-file-path>' % (__file__)
		sys.exit(1)
	handle(sys.argv[1])

def main2():
	for line in sys.stdin:
		handle(line)
		#sys.stdout.write(line)

def main3():
	line = sys.stdin.read()
	handle(line)

if __name__ == '__main__':
	try:  	
		main2()
	except KeyboardInterrupt:
		print 'user interrupt!!'
		sys.exit(0)
	except:
		print 'unknown exception!!'
		sys.exit(0)
