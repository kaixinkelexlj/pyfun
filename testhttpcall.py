#-*- coding: UTF-8 -*-
import __init__
import urllib
import urllib2
import json
import sys'''test url:http://api.waptest.taobao.com/rest/api3.do?sign=14c6043d9e1b68276c4c99e08de7cc21&sid=&ttid=123%40taobao_android_1.0&v=1.0&t=1445825118&imei=123456789012345&api=com.de.ylb.gw.hello&imsi=123456789012345&appKey=4272&data=%7B%22data%22%3A%22empty%22%7D&deviceId=72e7566255dce0fa6ec6131fc18f8d61c47e59e9'''

reload(sys)
sys.setdefaultencoding('utf-8')

def main():	checkArgs() 	send_list = []
	url = sys.argv[1]	print "call %s..." % url
	values = {			  'token':'n1xb053wjhqft2ri',
			  'rid':5,
			  'content':json.dumps(send_list, ensure_ascii=False)
    }
	data = urllib.urlencode(values)
	print data	try:		proxy = urllib2.ProxyHandler({'http': '127.0.0.1:8888'})		opener = urllib2.build_opener(proxy)		urllib2.install_opener(opener)		#req = urllib2.Request(url, data)		req = urllib2.Request(url)		response = urllib2.urlopen(req)		info_page = response.read()		print info_page	except urllib2.URLError, e:		print 'url call error:%s' % str(e)	finally:		print '##########call[%s]end~~~~~~~~~~~~~~~~~~~~' % (url)

def checkArgs():
	if len(sys.argv) < 2:
		print 'usage:\npy %s <url>' % __file__
		sys.exit(1)
if __name__ == '__main__':
	main() 
