#-*- coding: utf-8 -*-

import __init__

import sys
import os
import re

reload(sys)
sys.setdefaultencoding('utf-8')

sourceFile = r'c:\Users\lujun.xlj\Desktop\group.csv'
sqlFile = r'c:\Users\lujun.xlj\Desktop\updatechannelpid.sql'
#template = '''insert ignore into yw_dict_channel(gmt_create,gmt_modified,channel,alimama_pid,type,channel_name_cn,id_card_no,alipay_account,qr_code_url,channel_url,channel_short_url,status)values(now(),now(),'%s','%s',0,'%s',null,null,null,null,null,1)'''
template = '''
	update yw_dict_channel set pid = %s where channel = '%s'
'''

def main():
	if os.path.exists(sqlFile):
		os.remove(sqlFile)
	f = open(sourceFile)
	target = open(sqlFile, 'w+')
	for line in f.readlines():
		if not line:
			continue
		arr = re.sub(r'[\r\n]','',line).split(',');
		newLine = template % (arr[0].strip(), arr[1].strip())
		print newLine
		target.write(newLine + "\n")
		
	f.close()
	target.close()


if __name__ == '__main__':
    main()