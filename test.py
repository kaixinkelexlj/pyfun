#!/usr/bin/python
#coding=utf-8

from datetime import *

def testReadArgs():
	name = '';
	while not name:
		name = raw_input('give me args---');
	print 'args is %s' %name

def testJoin():
	a = 'x','l','j'
	print '|'.join(a);
	try:
		a.join('**');
	except:
		print 'error join !!'
	else:
		'**'.join(a);
	finally:
		print 'OMG!!'

def test():
	print 'hello python!!';
        
	a = r'c:\\xlj';
        print a;
	b = 'c:\\xlj'
	print b;

def testFile():
	f = open('io.py','r')
	print f.read()
	
	
def printParams(x, y, z, *list, **dict):
	print x,y,z
	print list
	print dict

def testDatetime():
	print datetime.today().time()
	
	
def main():
	#printParams(1,2,3,4,5,6,7,8,9,foo=1,bar=2)
	testDatetime()

if __name__ == '__main__':
    main()
