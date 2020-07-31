# coding=utf-8
import json
import re
import sys
import urllib2
from collections import namedtuple
from time import time

reload(sys)
sys.setdefaultencoding('utf8')


def chartdata():
    req = urllib2.Request('http:#data.weibo.com/index/ajax/getchartdata?month=6&__rnd=1500885369052')
    req.add_header("Host", "data.weibo.com");
    req.add_header("User-Agent",
                   "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36")
    req.add_header("Cookie", 'PHPSESSID=a4e3q2tuopvn9bfoje9t1mhq46; WEB3=d95be79b032239034fa1bc8b48d4f9f5')
    req.add_header("Referer", "http:#data.weibo.com/index/hotword?wid=13PzKl9zx&wname=%E5%88%98%E5%BE%B7%E5%8D%8E")

    resp = urllib2.urlopen(req)
    content = resp.read()
    print content


def index():
    req = urllib2.Request(
        "http:#data.weibo.com/index/hotword?wid=4f5pcFYS4vcR&wname=%E4%B8%89%E7%94%9F%E4%B8%89%E4%B8%96")
    req.add_header("Host", "data.weibo.com")
    req.add_header("User-Agent",
                   "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36' -H 'Content-Type: application/x-www-form-urlencoded' -H 'Accept: */*' -H 'Referer: http:#data.weibo.com/index/hotword?wid=13PzKl9zx&wname=%E5%88%98%E5%BE%B7%E5%8D%8E")

    resp = urllib2.urlopen(req)
    print resp.headers


def json2object(jsonString):
    try:
        from types import SimpleNamespace as Namespace
    except ImportError:
        # Python 2.x fallback
        from argparse import Namespace

    # x = json.loads(jsonString, object_hook=lambda d: Namespace(**d))
    def _json_object_hook(d):
        return namedtuple('X', d.keys())(*d.values())

    x = json.loads(jsonString, object_hook=_json_object_hook)

    return x


def getsession():
    req = urllib2.Request(
        "http:#data.weibo.com/index/hotword?wid=4f5pcFYS4vbS&wname=%E4%B8%89%E7%94%9F%E4%B8%89%E4%B8%96")
    resp = urllib2.urlopen(req);
    ss = resp.headers["Set-Cookie"]
    print ss
    # ss = 'PHPSESSID=h0rtvvicmbn6s1qfmghdumut93; path=/, WEB3=8b710afb399cd501a459af9c5a9c34f1;Path=/';
    m = re.match(r'.*WEB3=(\w+);.+', ss)
    if m:
        web3 = m.group(1)
    m = re.match(r'.*PHPSESSID=(\w+);.+', ss)
    if m:
        sid = m.group(1)
    if not web3 or not sid:
        print 'cookie absent'
        exit(1)
    return dict(sid=sid, web3=web3)


def crawl(keyword, session):
    sid = session["sid"]
    web3 = session["web3"]

    # 查关键字
    # http:#data.weibo.com/index/ajax/hotword?word=%25E5%25B0%258F%25E6%2597%25B6%25E4%25BB%25A3&flag=like&_t=0&__rnd=1500952913955
    keywordUrl = "http:#data.weibo.com/index/ajax/hotword?word=%s&flag=like&_t=0&__rnd=%s" % (keyword, time() * 1000)
    req = urllib2.Request(keywordUrl)
    req.add_header("Host", "data.weibo.com");
    req.add_header("User-Agent",
                   "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36")
    req.add_header("Cookie", 'PHPSESSID=%s; WEB3=%s' % (sid, web3))
    req.add_header("Referer", "http:#data.weibo.com/index/hotword?wid=13PzKl9zx&wname=%E5%88%98%E5%BE%B7%E5%8D%8E")
    resp = urllib2.urlopen(req)
    print resp
    respObj = json2object(resp.read())
    wdata = respObj.data[0]
    print "%s,%s" % (wdata.wid, wdata.wname)
    wid = wdata.wid

    # chartdata
    chartdataUrl = "http:#data.weibo.com/index/ajax/getchartdata?month=6&__rnd=%s" % (time() * 1000)
    req = urllib2.Request(chartdataUrl)
    req.add_header("Host", "data.weibo.com");
    req.add_header("User-Agent",
                   "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36")
    req.add_header("Cookie", 'PHPSESSID=%s; WEB3=%s' % (sid, web3))
    req.add_header("Referer", "http:#data.weibo.com/index/hotword?wid=%s" % (wid))
    resp = urllib2.urlopen(req)
    print resp
    respObj = json2object(resp.read())
    print respObj


def crawle2(keyword):
    keywordUrl = "http:#data.weibo.com/index/ajax/hotword?word=%s&flag=like&_t=0&__rnd=%s" % (keyword, time() * 1000)
    req = urllib2.Request(keywordUrl)
    req.add_header("Host", "data.weibo.com");
    req.add_header("User-Agent",
                   "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36")
    req.add_header("Referer", "http:#data.weibo.com/index")
    resp = urllib2.urlopen(req)
    print resp
    ss = resp.headers["Set-Cookie"]
    print ss
    # ss = 'PHPSESSID=h0rtvvicmbn6s1qfmghdumut93; path=/, WEB3=8b710afb399cd501a459af9c5a9c34f1;Path=/';
    m = re.match(r'.*WEB3=(\w+);.+', ss)
    if m:
        web3 = m.group(1)
    if not web3:
        print "get cookie web3 error"
        exit(1)
    respObj = json2object(resp.read())
    wdata = respObj.data[0]
    print "%s,%s" % (wdata.wid, wdata.wname)

    hotwordUrl = "http:#data.weibo.com/index/hotword?wid=%s&wname=%s" % (wdata.wid, wdata.wname)
    print hotwordUrl
    req = urllib2.Request(hotwordUrl)
    req.add_header("Host", "data.weibo.com");
    req.add_header("User-Agent",
                   "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36")

    req.add_header("Cookie", 'WEB3=%s;' % (web3))
    req.add_header("Referer", "http:#data.weibo.com/index")
    resp = urllib2.urlopen(req)
    print resp.headers
    ss = resp.headers["Set-Cookie"]
    print ss
    m = re.match(r'.*PHPSESSID=(\w+);.+', ss)
    if m:
        sid = m.group(1)
    if not sid:
        print "get cookie web3 error"
        exit(1)
    print "web3=%s, sid=%s" % (web3, sid)

    chartdataUrl = "http:#data.weibo.com/index/ajax/getchartdata?month=6&__rnd=%s" % (time() * 1000)
    req = urllib2.Request(chartdataUrl)
    req.add_header("Host", "data.weibo.com");
    req.add_header("User-Agent",
                   "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36")
    req.add_header("Cookie", 'PHPSESSID=%s; WEB3=%s' % (sid, web3))
    req.add_header("Referer", hotwordUrl)
    resp = urllib2.urlopen(req)
    print resp
    respObj = json2object(resp.read())
    print respObj.keyword[0]
    print respObj.data


def chartonly(web3, sid):
    chartdataUrl = "http:#data.weibo.com/index/ajax/getchartdata?month=6&__rnd=%s" % (time() * 1000)
    req = urllib2.Request(chartdataUrl)
    req.add_header("Host", "data.weibo.com");
    req.add_header("User-Agent",
                   "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36")
    req.add_header("Cookie", 'PHPSESSID=%s; WEB3=%s' % (sid, web3))
    req.add_header("Referer", "http:#data.weibo.com/index/hotword?wid=4f5pcFYS4vcV&wname=三生三世")
    resp = urllib2.urlopen(req)
    print resp
    respObj = json2object(resp.read())
    print respObj.keyword[0]
    print respObj.data


def crawle3(keyword, begindate, enddate):
    indexUrl = "http:#data.weibo.com/index"
    req = urllib2.Request(indexUrl)
    req.add_header("Host", "data.weibo.com")
    req.add_header("User-Agent",
                   "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36")

    resp = urllib2.urlopen(req)
    ss = resp.headers["Set-Cookie"]
    print ss
    m = re.match(r'.*WEB3=(\w+);.+', ss)
    if m:
        web3 = m.group(1)
    if not web3:
        print "get cookie web3 error"
        exit(1)

    keywordUrl = "http:#data.weibo.com/index/ajax/contrast?key2=%s&key3=&key4=&key5=&key6=" % (
        keyword)
    req = urllib2.Request(keywordUrl)
    req.add_header("Host", "data.weibo.com")
    req.add_header("User-Agent",
                   "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36")
    req.add_header("Referer", "http:#data.weibo.com/index")
    req.add_header("Cookie", "WEB3=%s;" % (web3))
    resp = urllib2.urlopen(req)
    respObj = json2object(resp.read())
    wid = respObj.data.key2.id
    print wid
    ss = resp.headers["Set-Cookie"]
    print ss
    m = re.match(r'.*PHPSESSID=(\w+);.+', ss)
    if m:
        sid = m.group(1)
    if not sid:
        print "get cookie web3 error"
        exit(1)

    keywordUrl = "http:#data.weibo.com/index/ajax/getchartdata?wid=%s&sdate=%s&edate=%s&__rnd=%s" % (
    wid, begindate, enddate, time() * 1000)
    req = urllib2.Request(keywordUrl)
    req.add_header("Host", "data.weibo.com")
    req.add_header("User-Agent",
                   "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36")
    req.add_header("Referer", "http:#data.weibo.com/index")
    req.add_header("Cookie", "WEB3=%s;PHPSESSID=%s" % (web3, sid))
    resp = urllib2.urlopen(req)
    print resp.read()


# crawle2("杨幂")
# crawle2("三生三世")
# "WEB3" -> "3c497a8c16cce6333cb20bd07cf296ff"
# "PHPSESSID" -> "97ld5vtck4i1cfoi9ch89trim0"
# chartonly(web3="3c497a8c16cce6333cb20bd07cf296ff", sid="97ld5vtck4i1cfoi9ch89trim0")
crawle3("绣春刀2", begindate="2017-01-01", enddate="2017-07-31")
