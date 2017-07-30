#-*- coding: utf-8 -*-

import __init__

import sys
import os
import re

reload(sys)
sys.setdefaultencoding('utf-8')

dataRoot = r'C:\Users\lujun.xlj\Desktop\data'
group = dataRoot + r'\dictgroup.csv'
dictchannel = dataRoot + r'\channelupdate.csv'
sqlFile = dataRoot + r'dictchannel-and-group.sql'

sqlChannel = '''
update yw_dict_channel set pid = %s,p_name = '%s' where channel = '%s';
'''

sqlGroup = '''
insert into yw_dict_channel_group(id,gmt_create,gmt_modified,name,pid,creator,last_update_by)
		values(%s,now(),now(),'%s',0,'sys','sys');
'''

groupDict = {}
channelList = []

def genGroup():
	f = open(group)
	global groupDict
	for line in f.readlines():
		if not line:
			continue
		arr = re.sub(r'[\r\n]','',line).split(',');
		groupDict[arr[1].strip()] = arr[0].strip()
	f.close()

def readChannel():
	f = open(dictchannel)
	global channelList
	for line in f.readlines():
		if not line:
			continue
		channelList.append(line)
	f.close()

def genSql():
	if os.path.exists(sqlFile):
		os.remove(sqlFile)
	target = open(sqlFile, 'w+')
	
	for key,val in groupDict.iteritems():
		line = sqlGroup % (val,key)
		print line
		target.write(line + '\n')
	for line in channelList:
		arr = line.split(',')
		line = sqlChannel % (groupDict.get(arr[5].strip()), arr[5].strip(), arr[1].strip())
		print line
		target.write(line + '\n')
	
	target.close()

def main():
	genGroup()
	readChannel()
	genSql()
	
if __name__ == '__main__':
    main()