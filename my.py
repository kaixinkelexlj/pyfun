#!/usr/bin/python
#coding=utf-8
import sys
import operator

word2count = {}

for line in sys.stdin:
	line = line.strip()
	word,count = line.split()
	try:
		count = int(count)
		word2count[word] = word2count.get(word,0) + count
	except valueError:
		pass

sorted_word2count = sorted(word2count.items(),key=operator.itemgetter(0))

for word,count in sorted_word2count:
	print "%s\t%s" % (word,count)
