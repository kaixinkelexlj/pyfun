#-*- coding: utf-8 -*-

import __init__

import sys
import os
import re

reload(sys)
sys.setdefaultencoding('utf-8')

sourceFile = r'c:\Users\lujun.xlj\Desktop\libradata.txt'
sqlFile = r'c:\Users\lujun.xlj\Desktop\channelinit.sql'
#template = '''insert ignore into yw_dict_channel(gmt_create,gmt_modified,channel,alimama_pid,type,channel_name_cn,id_card_no,alipay_account,qr_code_url,channel_url,channel_short_url,status)values(now(),now(),'%s','%s',0,'%s',null,null,null,null,null,1)'''
template = '''
	insert ignore into yw_libra_item(gmt_create,gmt_modified,item_id,item_name,libra_reserve_price,libra_prom_price,libra_item_title,libra_item_picurl,libra_item_manifesto,ts_last_update,gmt_last_update,status,price_source,prom_price_source,status_memo,libra_status,libra_content_id,libra_block_id,libra_application_id,gmt_libra_block_start,gmt_libra_block_end,
		libra_discount,libra_discount_source)
	values(now(),now(),'%s','%s-name',100,'%s','test','http://test','test',12345,12345,1,'111','111','memo','2',37120091080,46660421080,999,null,null,
		0,null);
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
		newLine = template % (arr[0], arr[0], arr[1])
		print newLine
		target.write(newLine + "\n")
		
	f.close()
	target.close()


if __name__ == '__main__':
    main()