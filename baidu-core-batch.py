#-*- coding: UTF-8 -*-
import __init__
import datetime
from datetime import datetime as xdatetime
from utils import db
import urllib
import urllib2
import json
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

def main():
    #today = datetime.date.today()
    #start_day = today-datetime.timedelta(3)
    #end_day = today-datetime.timedelta(1)   
   
    checkArgs() 

    start_day = xdatetime.strptime(sys.argv[1],'%Y-%m-%d')
    end_day = xdatetime.strptime(sys.argv[2], '%Y-%m-%d')

    print '''start %s,end %s''' % (int(datetime.date.strftime(start_day,'%Y%m%d')),int(datetime.date.strftime(end_day,'%Y%m%d')))    

    conn = db.connect(db.niux_dw)
    conn.set_character_set('utf8')
    cur = conn.cursor()
    send_list = []
    sql = '''select date, sid, value, cn_name, sid_type, update_time from buffet_etl_mysql where date between %s and %s;
    ''' % (int(datetime.date.strftime(start_day,'%Y%m%d')),int(datetime.date.strftime(end_day,'%Y%m%d')))
    cur.execute(sql)
    data = cur.fetchall()
    for item in data:
        date = int(item[0])
        sid = int(item[1])
        value = float(item[2])
        cn_name = str(item[3])
        sid_type = str(item[4])
        update_time = str(item[5])
        send_list.append({'sid':sid,'sid_type':'num','date':date,'value':value})
    print send_list
    #url = 'http://ph.baidu.com/pharos/buffet_api/v1/stat/data'
    url = 'http://10.48.29.85/pharos/buffet_api/v1/stat/data'
    values = {
              'token':'n1xb053wjhqft2ri',
              'rid':5,
              'content':json.dumps(send_list, ensure_ascii=False)
              }
    data = urllib.urlencode(values)
    print data
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    info_page = response.read()
    print info_page

def checkArgs():
    if len(sys.argv) < 3:
        print 'usage:\npython baidu-core-batch.py start-time end-time,time format %Y-%m-%d'
        sys.exit(1)

def test():
    checkArgs()
    start_day = xdatetime.strptime(sys.argv[1],'%Y-%m-%d')
    end_day = xdatetime.strptime(sys.argv[2], '%Y-%m-%d')

    print '''start %s,end %s''' % (int(datetime.date.strftime(start_day,'%Y%m%d')),int(datetime.date.strftime(end_day,'%Y%m%d'))
)
if __name__ == '__main__':
    main() 
