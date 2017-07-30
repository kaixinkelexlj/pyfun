#-*- coding: utf-8 -*-

import __init__

import sys
import os
import shutil

reload(sys)
sys.setdefaultencoding('utf-8')

rootDir = r'F:\workspace\Just4Fun\taobao-hsf.sar'
distDir = r'F:\workspace\Just4Fun\lib\hsf'

def test():
	print rootDir
	list_dirs = os.walk(rootDir)
	for root, dirs, files in list_dirs:
		'''
		for d in dirs:
			print os.path.join(root, d)
		'''
		for f in files:
			if f.endswith('.jar'):
				print os.path.join(root, f)
				shutil.copy(os.path.join(root, f), distDir)
def main():
	test()

if __name__ == '__main__':
    main()
