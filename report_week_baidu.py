#-*- coding: UTF-8 -*-
import __init__
from utils import dba
import datetime
from utils import email_tool
import re
import sys

def strConv(s):  
    s =  str(s)
    while True:
        (s,count) = re.subn(r"(\d)(\d{3})((:?,\d\d\d)*)$",r"\1,\2\3",s)
        if count == 0 : break
    return s

def get_data(day, cur):
    result_dict = {1:[0,0,0,0,0,0],
                   2:[0,0,0,0,0,0],
                   3:[0,0,0,0,0,0],
                   4:[0,0,0,0,0,0],
                   5:[0,0,0,0,0,0]}
    sql = '''select ifnull(sum(unique_visit),0) from stat_daily_report where date = %s and type = 0;''' % (int(str(day)[:4]+str(day)[5:7]+str(day)[8:10]))
    cur.execute(sql)
    data = cur.fetchone()
    if data is not None and data[0] is not None:
        result_dict[1][0] = int(data[0])
    sql = '''select count(distinct oid), sum(total_money)/1000, count(distinct user_id), sum(if(is_new_custom=1,1,0)) from r_order_base where pay_time between '%s 00:00:00' 
    and '%s 23:59:59' and platform_type = 0 and deal_id > 0 and status = 1 and total_money > 0;''' % (str(day),str(day))
    cur.execute(sql)
    data = cur.fetchone()
    if data is not None:
        if data[0] is not None:
            result_dict[2][0] = int(data[0])
        if data[1] is not None:
            result_dict[3][0] = int(data[1])
        if data[2] is not None:
            result_dict[4][0] = int(data[2])
        if data[3] is not None:
            result_dict[5][0] = int(data[3])
    sql = '''select active_user from data_umeng_ga_daily where date = %s and app = 'WAP';''' % (int(str(day)[:4]+str(day)[5:7]+str(day)[8:10]))
    cur.execute(sql)
    data = cur.fetchone()
    if data is not None and data[0] is not None:
        result_dict[1][1] = int(data[0])
    sql = '''select count(distinct oid), sum(total_money)/1000, count(distinct user_id), sum(if(is_new_custom=1,1,0)) from r_order_base where pay_time between '%s 00:00:00' 
    and '%s 23:59:59' and platform_type = 1 and deal_id > 0 and status = 1 and total_money > 0;''' % (str(day),str(day))
    cur.execute(sql)
    data = cur.fetchone()
    if data is not None:
        if data[0] is not None:
            result_dict[2][1] = int(data[0])
        if data[1] is not None:
            result_dict[3][1] = int(data[1])
        if data[2] is not None:
            result_dict[4][1] = int(data[2])
        if data[3] is not None:
            result_dict[5][1] = int(data[3])
    sql = '''select active_user from data_umeng_ga_daily where date = %s and app = '糯米网_iPad';''' % (int(str(day)[:4]+str(day)[5:7]+str(day)[8:10]))
    cur.execute(sql)
    data = cur.fetchone()
    if data is not None and data[0] is not None:
        result_dict[1][2] = int(data[0])
    sql = '''select count(distinct o.oid), sum(o.total_money)/1000, count(distinct o.user_id), sum(if(o.is_new_custom=1,1,0)) from r_order_base as o inner join 
    r_order_mobile as om on om.order_id = o.oid where o.pay_time between '%s 00:00:00' and '%s 23:59:59' and o.platform_type = 2 and om.platform = 'ipad' 
    and o.deal_id > 0 and o.status = 1 and o.total_money > 0;
    ''' % (str(day),str(day))
    cur.execute(sql)
    data = cur.fetchone()
    if data is not None:
        if data[0] is not None:
            result_dict[2][2] = int(data[0])
        if data[1] is not None:
            result_dict[3][2] = int(data[1])
        if data[2] is not None:
            result_dict[4][2] = int(data[2])
        if data[3] is not None:
            result_dict[5][2] = int(data[3])
    sql = '''select ifnull(sum(active_user),0) from data_umeng_ga_daily where date = %s and app != 'WAP';''' % (int(str(day)[:4]+str(day)[5:7]+str(day)[8:10]))
    cur.execute(sql)
    data = cur.fetchone()
    if data is not None and data[0] is not None:
        result_dict[1][3] = int(data[0])
    sql = '''select count(distinct o.oid), sum(o.total_money)/1000, count(distinct o.user_id), sum(if(o.is_new_custom=1,1,0)) from r_order_base as o inner join 
    r_order_mobile as om on om.order_id = o.oid where o.pay_time between '%s 00:00:00' and '%s 23:59:59' and o.platform_type = 2 and o.deal_id > 0 and o.status = 1 
    and o.total_money > 0;''' % (str(day),str(day))
    cur.execute(sql)
    data = cur.fetchone()
    if data is not None:
        if data[0] is not None:
            result_dict[2][3] = int(data[0])
        if data[1] is not None:
            result_dict[3][3] = int(data[1])
        if data[2] is not None:
            result_dict[4][3] = int(data[2])
        if data[3] is not None:
            result_dict[5][3] = int(data[3])
    sql = '''select ifnull(sum(active_user),0) from data_umeng_ga_daily where date = %s and app in ('糯米网_Android','糯米酒店_Android');
    ''' % (int(str(day)[:4]+str(day)[5:7]+str(day)[8:10]))
    cur.execute(sql)
    data = cur.fetchone()
    if data is not None and data[0] is not None:
        result_dict[1][4] = int(data[0])
    sql = '''select count(distinct o.oid), sum(o.total_money)/1000, count(distinct o.user_id), sum(if(o.is_new_custom=1,1,0)) from r_order_base as o inner join 
    r_order_mobile as om on om.order_id = o.oid where o.pay_time between '%s 00:00:00' and '%s 23:59:59' and o.platform_type = 2 and om.platform = 'android' and 
    o.deal_id > 0 and o.status = 1 and o.total_money > 0;
    ''' % (str(day),str(day))
    cur.execute(sql)
    data = cur.fetchone()
    if data is not None:
        if data[0] is not None:
            result_dict[2][4] = int(data[0])
        if data[1] is not None:
            result_dict[3][4] = int(data[1])
        if data[2] is not None:
            result_dict[4][4] = int(data[2])
        if data[3] is not None:
            result_dict[5][4] = int(data[3])
    sql = '''select active_user from data_umeng_ga_daily where date = %s and app = '糯米网_iPhone';''' % (int(str(day)[:4]+str(day)[5:7]+str(day)[8:10]))
    cur.execute(sql)
    data = cur.fetchone()
    if data is not None and data[0] is not None:
        result_dict[1][5] = int(data[0])
    sql = '''select count(distinct o.oid), sum(o.total_money)/1000, count(distinct o.user_id), sum(if(o.is_new_custom=1,1,0)) from r_order_base as o inner join 
    r_order_mobile as om on om.order_id = o.oid where o.pay_time between '%s 00:00:00' and '%s 23:59:59' and o.platform_type = 2 and om.platform in ('ios','iphone') 
    and o.deal_id > 0 and o.status = 1 and o.total_money > 0;
    ''' % (str(day),str(day))
    cur.execute(sql)
    data = cur.fetchone()
    if data is not None:
        if data[0] is not None:
            result_dict[2][5] = int(data[0])
        if data[1] is not None:
            result_dict[3][5] = int(data[1])
        if data[2] is not None:
            result_dict[4][5] = int(data[2])
        if data[3] is not None:
            result_dict[5][5] = int(data[3])
    return result_dict

def check_data(in_dict, flag):
    #进行非零校验
    result_flag = 1
    for key, value in in_dict.iteritems():
        for i in range(len(value)):
            if value[i] == 0 and flag is True:
                if key != 5:
                    result_flag = 0
                    value[i] = '此项不应该为零%s' % strConv(value[i])
                else:
                    result_flag = 0
                    value[i] = '此项不应该为零%2.2f%%' % value[i]
            else:
                if key != 5:
                    value[i] = '%s' % strConv(value[i])
                else:
                    value[i] = '%2.2f%%' % value[i]
    return [in_dict, result_flag]

def main():
    email_data = '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">'''
    email_data += '''<html xmlns="http://www.w3.org/1999/xhtml">'''
    email_data += '''<head><meta http-equiv="Content-Type" content="text/html; charset=utf-8" /><title>全国日报</title></head>'''
    email_data += '''<body>'''
    email_one = '''<h3>1、DAU</h3><table width="100%" border="0" cellspacing="1" cellpadding="0" bgcolor="#333333" style="font-size:13px">
    <tr bgcolor="#CEF3FF" height="30" align="center"><td>日期</td><td>PC</td><td>webapp</td><td>ipad端</td><td>手机客户端-整体</td><td>手机客户端-andr.</td><td>手机客户端-ios</td>'''
    email_two = '''<h3>2、订单量</h3><table width="100%" border="0" cellspacing="1" cellpadding="0" bgcolor="#333333" style="font-size:13px">
    <tr bgcolor="#CEF3FF" height="30" align="center"><td>日期</td><td>PC</td><td>webapp</td><td>ipad端</td><td>手机客户端-整体</td><td>手机客户端-andr.</td><td>手机客户端-ios</td>'''
    email_three = '''<h3>3、流水</h3><table width="100%" border="0" cellspacing="1" cellpadding="0" bgcolor="#333333" style="font-size:13px">
    <tr bgcolor="#CEF3FF" height="30" align="center"><td>日期</td><td>PC</td><td>webapp</td><td>ipad端</td><td>手机客户端-整体</td><td>手机客户端-andr.</td><td>手机客户端-ios</td>'''
    email_four = '''<h3>4、购买用户数</h3><table width="100%" border="0" cellspacing="1" cellpadding="0" bgcolor="#333333" style="font-size:13px">
    <tr bgcolor="#CEF3FF" height="30" align="center"><td>日期</td><td>PC</td><td>webapp</td><td>ipad端</td><td>手机客户端-整体</td><td>手机客户端-andr.</td><td>手机客户端-ios</td>'''
    email_five = '''<h3>5、新用户购买占比</h3><table width="100%" border="0" cellspacing="1" cellpadding="0" bgcolor="#333333" style="font-size:13px">
    <tr bgcolor="#CEF3FF" height="30" align="center"><td>日期</td><td>PC</td><td>webapp</td><td>ipad端</td><td>手机客户端-整体</td><td>手机客户端-andr.</td><td>手机客户端-ios</td>'''
    today = datetime.date.today()
    yesterday = today-datetime.timedelta(2)
    day = yesterday
    conn = dba.connect(dba.niux_dw, False)
    conn.set_character_set('utf8')
    cur = conn.cursor()
    flag = 1
    check_flag = True
    send_flag = 1
    if len(sys.argv) == 2 and sys.argv[1] == 'True':
        check_flag = False
    for i in range(7):
        result_data = get_data(day, cur)
        if flag == 0:
            email_one += '''<tr bgcolor="#E4EEF8" height="20" align="right">'''
            email_two += '''<tr bgcolor="#E4EEF8" height="20" align="right">'''
            email_three += '''<tr bgcolor="#E4EEF8" height="20" align="right">'''
            email_four += '''<tr bgcolor="#E4EEF8" height="20" align="right">'''
            email_five += '''<tr bgcolor="#E4EEF8" height="20" align="right">'''
            flag = 1
        else:
            email_one += '''<tr bgcolor="#ffffff" height="20" align="right">'''
            email_two += '''<tr bgcolor="#ffffff" height="20" align="right">'''
            email_three += '''<tr bgcolor="#ffffff" height="20" align="right">'''
            email_four += '''<tr bgcolor="#ffffff" height="20" align="right">'''
            email_five += '''<tr bgcolor="#ffffff" height="20" align="right">'''
            flag = 0
        for j in range(len(result_data[5])):
            if result_data[4][j] != 0:
                result_data[5][j] = result_data[5][j]*100.0/result_data[4][j]
            else:
                result_data[5][j] = 0.0
        check_result = check_data(result_data, check_flag)
        result_data = check_result[0]
        if send_flag != 0:
            send_flag = check_result[1]
        email_one += '''<td>%s/%s/%s</td><td>''' % (day.year,day.month,day.day) + '''</td><td>'''.join(result_data[1]) + '''</td>'''
        email_two += '''<td>%s/%s/%s</td><td>''' % (day.year,day.month,day.day) + '''</td><td>'''.join(result_data[2]) + '''</td>'''
        email_three += '''<td>%s/%s/%s</td><td>''' % (day.year,day.month,day.day) + '''</td><td>'''.join(result_data[3]) + '''</td>'''
        email_four += '''<td>%s/%s/%s</td><td>''' % (day.year,day.month,day.day) + '''</td><td>'''.join(result_data[4]) + '''</td>'''
        email_five += '''<td>%s/%s/%s</td><td>''' % (day.year,day.month,day.day) + '''</td><td>'''.join(result_data[5]) + '''</td>'''
        day = day-datetime.timedelta(1)
        email_one += '''</tr>'''
        email_two += '''</tr>'''
        email_three += '''</tr>'''
        email_four += '''</tr>'''
        email_five += '''</tr>'''
    email_one += '''</table>'''
    email_two += '''</table>'''
    email_three += '''</table>'''
    email_four += '''</table>'''
    email_five += '''</table>'''
    email_data += email_one
    email_data += email_two
    email_data += email_three
    email_data += email_four
    email_data += email_five
    email_data += '''</body></html>'''
    day = day+datetime.timedelta(1)
    
    if send_flag == 1:
        email_dict = {}
        email_dict['to'] = '''shangguobin@baidu.com, mapingping@baidu.com, huyue@baidu.com, shenli@baidu.com, nuomi.tongji@renren-inc.com, nuomi.ba@renren-inc.com, LBS-BI-Tuangou@baidu.com'''
        email_dict['subject']  = '糯米网周简报--百度（V1版）%s/%s/%s-%s/%s/%s'.decode('utf-8')%(day.year,day.month,day.day,yesterday.year,yesterday.month,yesterday.day)
        email_dict['text'] = ''
        email_dict['html'] = email_data
        email_dict['path'] = ''
        email_tool.process(email_dict)
    else:
        email_dict = {}
        email_dict['to'] = '''nuomi.tongji@renren-inc.com'''
        email_dict['subject']  = 'ERROR糯米网周简报--百度（V1版）%s/%s/%s-%s/%s/%s'.decode('utf-8')%(day.year,day.month,day.day,yesterday.year,yesterday.month,yesterday.day)
        email_dict['text'] = ''
        email_dict['html'] = email_data
        email_dict['path'] = ''
        email_tool.process(email_dict)
    
if __name__ == '__main__':
    main()