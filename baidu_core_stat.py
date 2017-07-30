#-*- coding: UTF-8 -*-
import __init__
import datetime
from utils import db
import urllib
import urllib2
import json
import sys
from utils import email_tool

reload(sys)
sys.setdefaultencoding('utf-8')

#register_url = 'http://pharos.baidu.com/pharos/buffet_api/v1/stat/register'
#push_url = 'http://pharos.baidu.com/pharos/buffet_api/v1/stat/data'

register_url = 'http://10.52.144.77/pharos/buffet_api/v1/stat/register'
push_url = 'http://10.52.144.77/pharos/buffet_api/v1/stat/data'

file_dict = {6122:{
                    0: {'name': '站点', 'type': 'string'},
                    1: {'name': '一级品类', 'type': 'string'},
                    2: {'name': '二级品类', 'type': 'string'},
                    3: {'name': 'SKU', 'type': 'int'},
                    4: {'name': 'POI', 'type': 'int'},
                    5: {'name': '商户', 'type': 'int'}, 
                    6: {'name': '流水', 'type': 'float'},
                    7: {'name': '产生流水SKU数', 'type': 'int'},
                    8: {'name': '单均流水贡献', 'type': 'float'}
                    },
        6123:{
                    0: {'name': '一级渠道', 'type': 'string'},
                    1: {'name': '二级渠道', 'type': 'string'},
                    2: {'name': 'UV', 'type': 'int'},
                    3: {'name': '订单', 'type': 'int'},
                    4: {'name': '流水', 'type': 'int'},
                    5: {'name': '成单率', 'type': 'float'},
                    6: {'name': '客单价', 'type': 'float'}
                    },
        6124:{
                    0: {'name': '一级渠道', 'type': 'string'},
                    1: {'name': 'UV', 'type': 'int'}
                    },
        6125:{
                    0: {'name': '分终端', 'type': 'string'},
                    1: {'name': '一级品类', 'type': 'string'},
                    2: {'name': '二级品类', 'type': 'string'},
                    3: {'name': '流水', 'type': 'float'},
                    4: {'name': '订单', 'type': 'int'},
                    5: {'name': '销量', 'type': 'int'},
                    6: {'name': '客单价', 'type': 'float'}
                    },
        6140:{
                    0: {'name': '一级品类', 'type': 'string'},
                    1: {'name': '二级品类', 'type': 'string'},
                    2: {'name': '毛收入', 'type': 'float'},
                    3: {'name': '毛利率', 'type': 'float'},
                    }
             }

sid_pid = {6001:[1010, 9999, '百糯UV数据'],
            6002:[1010, 9999, '百糯UV数据'],
            6003:[1010, 9999, '百糯UV数据'],
            6004:[1010, 9999, '百糯UV数据'],
            6005:[1010, 9999, '百糯UV数据'],
            6006:[1010, 9999, '百糯UV数据'],
            6007:[1010, 9999, '百糯UV数据'],
            6008:[1010, 9999, '百糯UV数据'],
            6009:[1010, 9999, '百糯UV数据'],
            6010:[1010, 9999, '百糯UV数据'],
            6011:[1010, 9999, '百糯UV数据'],
            6012:[2110, 9998, '百糯订单数据'],
            6013:[2110, 9998, '百糯订单数据'],
            6014:[2110, 9998, '百糯订单数据'],
            6015:[2110, 9998, '百糯订单数据'],
            6016:[2110, 9998, '百糯订单数据'],
            6017:[2110, 9998, '百糯订单数据'],
            6018:[2110, 9998, '百糯订单数据'],
            6019:[2110, 9998, '百糯订单数据'],
            6020:[2110, 9998, '百糯订单数据'],
            6021:[2110, 9998, '百糯订单数据'],
            6022:[2110, 9998, '百糯订单数据'],
            6023:[2110, 9998, '百糯订单数据'],
            6024:[2110, 9998, '百糯订单数据'],
            6025:[1010, 9997, '百糯流水数据'],
            6026:[1010, 9997, '百糯流水数据'],
            6027:[1010, 9997, '百糯流水数据'],
            6028:[1010, 9997, '百糯流水数据'],
            6029:[1010, 9997, '百糯流水数据'],
            6030:[1010, 9997, '百糯流水数据'],
            6031:[1010, 9997, '百糯流水数据'],
            6032:[1010, 9997, '百糯流水数据'],
            6033:[1010, 9997, '百糯流水数据'],
            6034:[1010, 9997, '百糯流水数据'],
            6035:[1010, 9997, '百糯流水数据'],
            6036:[1010, 9997, '百糯流水数据'],
            6037:[1010, 9997, '百糯流水数据'],
            6038:[1010, 9997, '百糯流水数据'],
            6069:[1010, 9997, '百糯流水数据'],
            6070:[1010, 9997, '百糯流水数据'],
            6071:[1010, 9997, '百糯流水数据'],
            6072:[1010, 9997, '百糯流水数据'],
            6073:[1010, 9997, '百糯流水数据'],
            6074:[1010, 9997, '百糯流水数据'],
            6075:[1010, 9997, '百糯流水数据'],
            6076:[1010, 9997, '百糯流水数据'],
            6077:[1010, 9997, '百糯流水数据'],
            6078:[1010, 9997, '百糯流水数据'],
            6079:[1010, 9997, '百糯流水数据'],
            6080:[1010, 9997, '百糯流水数据'],
            6081:[1010, 9997, '百糯流水数据'],
            6082:[1010, 9997, '百糯流水数据'],
            6083:[1010, 9997, '百糯流水数据'],
            6084:[1010, 9997, '百糯流水数据'],
            6039:[2110, 9996, '百糯购买用户数据'],
            6040:[2110, 9996, '百糯购买用户数据'],
            6041:[2110, 9996, '百糯购买用户数据'],
            6042:[2110, 9996, '百糯购买用户数据'],
            6043:[2110, 9996, '百糯购买用户数据'],
            6044:[2110, 9996, '百糯购买用户数据'],
            6045:[2110, 9996, '百糯购买用户数据'],
            6046:[2110, 9996, '百糯购买用户数据'],
            6047:[2110, 9996, '百糯购买用户数据'],
            6048:[2110, 9996, '百糯购买用户数据'],
            6049:[2110, 9996, '百糯购买用户数据'],
            6050:[2110, 9995, '百糯新客数据'],
            6051:[2110, 9995, '百糯新客数据'],
            6052:[2110, 9995, '百糯新客数据'],
            6053:[2110, 9995, '百糯新客数据'],
            6054:[2110, 9995, '百糯新客数据'],
            6055:[2110, 9995, '百糯新客数据'],
            6056:[2110, 9995, '百糯新客数据'],
            6057:[2110, 9995, '百糯新客数据'],
            6058:[2110, 9995, '百糯新客数据'],
            6059:[2110, 9995, '百糯新客数据'],
            6060:[2110, 9995, '百糯新客数据'],
            6061:[2110, 9995, '百糯新客数据'],
            6062:[2110, 9995, '百糯新客数据'],
            6063:[2110, 9994, '百糯新增数据'],
            6064:[2110, 9994, '百糯新增数据'],
            6065:[2110, 9994, '百糯新增数据'],
            6066:[2110, 9994, '百糯新增数据'],
            6067:[2110, 9994, '百糯新增数据'],
            6068:[2110, 9994, '百糯新增数据'],
            6085:[2110, 9994, '百糯新增数据'],
            6086:[2110, 9994, '百糯新增数据'],
            6087:[2110, 9994, '百糯新增数据'],
            6088:[2110, 9994, '百糯新增数据'],
            6089:[2110, 9994, '百糯新增数据'],
            6090:[2110, 9994, '百糯新增数据'],
            6091:[2110, 9993, '百糯竞品数据'],
            6092:[2110, 9993, '百糯竞品数据'],
            6093:[2110, 9993, '百糯竞品数据'],
            6094:[2110, 9993, '百糯竞品数据'],
            6095:[2110, 9993, '百糯竞品数据'],
            6096:[2110, 9993, '百糯竞品数据'],
            6097:[2110, 9993, '百糯竞品数据'],
            6098:[2110, 9993, '百糯竞品数据'],
            6099:[2110, 9993, '百糯竞品数据'],
            6100:[2110, 9993, '百糯竞品数据'],
            6101:[2110, 9993, '百糯竞品数据'],
            6102:[2110, 9993, '百糯竞品数据'],
            6103:[2110, 9993, '百糯竞品数据'],
            6104:[2110, 9993, '百糯竞品数据'],
            6105:[2110, 9993, '百糯竞品数据'],
            6106:[2110, 9993, '百糯竞品数据'],
            6107:[2110, 9993, '百糯竞品数据'],
            6108:[2110, 9993, '百糯竞品数据'],
            6126:[2110, 9993, '百糯竞品数据'],
            6127:[2110, 9993, '百糯竞品数据'],
            6128:[2110, 9993, '百糯竞品数据'],
            6129:[2110, 9993, '百糯竞品数据'],
            6130:[2110, 9993, '百糯竞品数据'],
            6131:[2110, 9993, '百糯竞品数据'],
            6122:[2110, 9992, '百糯多维数据'],
            6123:[2110, 9992, '百糯多维数据'],
            6124:[2110, 9992, '百糯多维数据'],
            6125:[2110, 9992, '百糯多维数据'],
            6140:[2110, 9992, '百糯多维数据'],
            6109:[2110, 9991, '百糯销量数据'],
            6110:[2110, 9991, '百糯销量数据'],
            6111:[2110, 9991, '百糯销量数据'],
            6112:[2110, 9991, '百糯销量数据'],
            6113:[2110, 9991, '百糯销量数据'],
            6114:[2110, 9991, '百糯销量数据'],
            6115:[2110, 9991, '百糯销量数据'],
            6116:[2110, 9991, '百糯销量数据'],
            6117:[2110, 9991, '百糯销量数据'],
            6118:[2110, 9991, '百糯销量数据'],
            6119:[2110, 9991, '百糯销量数据'],
            6120:[2110, 9991, '百糯销量数据'],
            6121:[2110, 9991, '百糯销量数据'],
            6132:[2110, 9990, '百糯商品数据'],
            6133:[2110, 9990, '百糯商品数据'],
            6134:[2110, 9990, '百糯商品数据'],
            6135:[2110, 9990, '百糯商品数据'],
            6136:[2110, 9990, '百糯商品数据'],
            6137:[2110, 9990, '百糯商品数据'],
            6138:[2110, 9990, '百糯商品数据'],
            6139:[2110, 9990, '百糯商品数据']}



def register_num(cur):
    register_list = []
    sql = '''select sid, cn_name, sid_type from dim_buffet_sid where push_type = 'num';'''
    cur.execute(sql)
    data = cur.fetchall()
    for item in data:
        sid = int(item[0])
        if not sid_pid.has_key(sid):
            continue
        cn_name = str(item[1])
        if sid_pid[sid][0] == 1010:
            register_list.append({'pid':sid_pid[sid][0],
                                  'tid':sid_pid[sid][1],
                                  'sid':sid,
                                  'tid_name':sid_pid[sid][2],
                                  'sid_type':'num',
                                  'sid_level':'high',
                                  'en_name':'Oliver',
                                  'cn_name':cn_name,
                                  'columns':{}})
        else:
            register_list.append({'pid':sid_pid[sid][0],
                                  'tid':sid_pid[sid][1],
                                  'sid':sid,
                                  'tid_name':sid_pid[sid][2],
                                  'sid_type':'num',
                                  'en_name':'Oliver',
                                  'cn_name':cn_name,
                                  'columns':{}})
    values = {
              'token':'n1xb053wjhqft2ri',
              'rid':5,
              'content':json.dumps(register_list, ensure_ascii=False)
              }
    data = urllib.urlencode(values)
    print data
    req = urllib2.Request(register_url, data)
    response = urllib2.urlopen(req)
    info_page = response.read()
    print info_page
    
def register_file(cur):
    register_list = []
    sql = '''select sid, cn_name, sid_type from dim_buffet_sid where push_type = 'file';''' 
    cur.execute(sql)
    data = cur.fetchall()
    for item in data:
        sid = int(item[0])
        if not file_dict.has_key(sid):
            continue
        if not sid_pid.has_key(sid):
            continue
        cn_name = str(item[1])
        sid_type = str(item[2])
        if sid_pid[sid][0] == 1010:
            register_list.append({'pid':sid_pid[sid][0],
                                  'tid':sid_pid[sid][1],
                                  'sid':sid,
                                  'tid_name':sid_pid[sid][2],
                                  'sid_type':'file',
                                  'sid_level':'high',
                                  'en_name':'Oliver',
                                  'cn_name':cn_name,
                                  'columns':file_dict[sid]})
        else:
            register_list.append({'pid':sid_pid[sid][0],
                                  'tid':sid_pid[sid][1],
                                  'sid':sid,
                                  'tid_name':sid_pid[sid][2],
                                  'sid_type':'file',
                                  'en_name':'Oliver',
                                  'cn_name':cn_name,
                                  'columns':file_dict[sid]})
    values = {
              'token':'n1xb053wjhqft2ri',
              'rid':5,
              'content':json.dumps(register_list, ensure_ascii=False)
              }
    data = urllib.urlencode(values)
    print data
    req = urllib2.Request(register_url, data)
    response = urllib2.urlopen(req)
    info_page = response.read()
    print info_page
    
def push_num(day,cur):
    send_list = []
    sql = '''select sid, value, cn_name, sid_type, update_time from buffet_etl_mysql where date = %s;
    ''' % (int(datetime.date.strftime(day,'%Y%m%d')))
    cur.execute(sql)
    data = cur.fetchall()
    for item in data:
        sid = int(item[0])
        value = float(item[1])
        if value == 0 and sid not in (6007, 6010, 6086, 6089):
            email_dict = {}
            email_dict['to'] = '''luan.dong@renren-inc.com.com'''
            email_dict['subject']  = '%s %s为0'.decode('utf-8') % (sid, int(datetime.date.strftime(day,'%Y%m%d')))
            email_dict['text'] = ''
            email_dict['html'] = ''
            email_dict['path'] = ''
            email_tool.process(email_dict)
            continue
        cn_name = str(item[2])
        sid_type = str(item[3])
        update_time = str(item[4])
        send_list.append({'sid':sid,'sid_type':'num','date':int(datetime.date.strftime(day,'%Y%m%d')),'value':value})
    print send_list
    values = {
              'token':'n1xb053wjhqft2ri',
              'rid':5,
              'content':json.dumps(send_list, ensure_ascii=False)
              }
    data = urllib.urlencode(values)
    print data
    req = urllib2.Request(push_url, data)
    response = urllib2.urlopen(req)
    info_page = response.read()
    print info_page

def push_file(day,cur,sid):
    send_list = []
    value_list = []
    if sid == 6125:
        sql = '''select case when ob.platform_type = 0 then 'PC' when ob.platform_type = 1 then 'WAP' when ob.platform_type = 2 then 'NA' end as '分终端', 
        deal.category_name_1 as '一级品类', deal.category_name_2 as '二级品类', sum(ob.total_money)/1000 as '流水', count(distinct ob.oid) as '订单', sum(ob.count) as '销量', 
        sum(ob.total_money)/count(distinct ob.oid)/1000 as '客单价' from r_order_base ob left join rpt_stat_all_deal deal on ob.deal_id = deal.deal_id 
        where ob.loaddate = %s group by ob.platform_type, deal.category_name_1, deal.category_name_2;''' % (int(datetime.date.strftime(day,'%Y%m%d')))
        cur.execute(sql)
        data = cur.fetchall()
        for item in data:
            value_list.append('\t'.join([str(item[0]), str(item[1]), str(item[2]), str(item[3]), str(item[4]), str(item[5]), str(item[6])]))
        send_list.append({'sid':sid,'sid_type':'file','date':int(datetime.date.strftime(day,'%Y%m%d')),'value':'\n'.join(value_list)})
    elif sid == 6122:
        sql = '''select a.site, a.category_name_1, a.category_name_2, a.SKU, a.POI, a.custom_count, ifnull(b.total_money,0), ifnull(b.deal_count,0), 
        ifnull(b.total_money,0)/ifnull(b.deal_count,0)/1000 from (select '糯米' as site, category_name_1, category_name_2, count(distinct stat.deal_id) as SKU, 
        count(distinct cf.firm_id) as POI, count(distinct cf.CUSTOM_ID) as custom_count from dw_m_day_online_deal deal left join rpt_stat_all_deal stat 
        on deal.deal_id = stat.deal_id left join t_merchant_deal_full rela on stat.deal_id = rela.deal_id left join crm_firm cf on cf.firm_id = rela.firm_id 
        where deal.date = %s and rela.firm_id is not null group by stat.category_id_1, stat.category_id_2, stat.category_name_1, stat.category_name_2 ) a 
        left join (select '糯米' as site, category_name_1, category_name_2, sum(deal.total_money)/1000 as total_money, count(distinct deal.deal_id) as deal_count 
        from rpt_day_deal deal left join rpt_stat_all_deal stat on deal.deal_id = stat.deal_id where deal.date = %s and deal.buy_count > 0 
        group by stat.category_id_1, stat.category_id_2, stat.category_name_1, stat.category_name_2) b on a.category_name_1 = b.category_name_1 and 
        a.category_name_2 = b.category_name_2 union all select a.site, a.category_name_1, a.category_name_2, a.SKU, a.POI, a.custom_count, ifnull(b.total_money,0), 
        ifnull(b.deal_count,0), ifnull(b.total_money,0)/ifnull(b.deal_count,0)/1000 from (select case when deal.site_id = 1 then '美团' when deal.site_id = 2 then '点评' 
        when deal.site_id = 3 then '窝窝' when deal.site_id = 9 then '拉手' end as site, case when category_name_1 is null or category_name_1 = '' then '未知' 
        else category_name_1 end as category_name_1, case when category_name_2 is null or category_name_2 = '' then '未知' else category_name_2 end as category_name_2, 
        if(deal.site_id != 1, 0, count(distinct stat.id)) as SKU, if(deal.site_id != 1, 0, count(distinct cf.firm_id)) as POI, 
        if(deal.site_id != 1, 0, count(distinct cf.CUSTOM_ID)) as custom_count from stat_rival_deal_sale deal left join stat_rival_deal stat 
        on deal.deal_id = stat.id and deal.site_id = stat.site_id left join stat_rival_deal_nuomi_shop rela on stat.id = rela.deal_id left join crm_firm cf 
        on cf.firm_id = rela.firm_id where deal.date = %s group by stat.category_id_1, stat.category_id_2, stat.category_name_1, stat.category_name_2, 
        deal.site_id) a left join (select case when deal.site_id = 1 then '美团' when deal.site_id = 2 then '点评' when deal.site_id = 3 then '窝窝' 
        when deal.site_id = 9 then '拉手' end as site, case when category_name_1 is null or category_name_1 = '' then '未知' else category_name_1 end as category_name_1, 
        case when category_name_2 is null or category_name_2 = '' then '未知' else category_name_2 end as category_name_2, 
        sum(deal.discount*deal.buy_count)/1000 as total_money, count(distinct deal.deal_id) as deal_count from stat_rival_deal_sale deal left join stat_rival_deal stat 
        on deal.deal_id = stat.id and deal.site_id = stat.site_id where deal.date = %s and deal.buy_count > 0 group by stat.category_id_1, stat.category_id_2, 
        stat.category_name_1, stat.category_name_2, deal.site_id ) b on a.category_name_1 = b.category_name_1 and a.category_name_2 = b.category_name_2;
        ''' % (int(datetime.date.strftime(day,'%Y%m%d')),int(datetime.date.strftime(day,'%Y%m%d')),int(datetime.date.strftime(day,'%Y%m%d')),
               int(datetime.date.strftime(day,'%Y%m%d')))
        cur.execute(sql)
        data = cur.fetchall()
        for item in data:
            value_list.append('\t'.join([str(item[0]), str(item[1]), str(item[2]), str(item[3]), str(item[4]), str(item[5]), str(item[6]), str(item[7]), str(item[8])]))
        send_list.append({'sid':sid,'sid_type':'file','date':int(datetime.date.strftime(day,'%Y%m%d')),'value':'\n'.join(value_list)})
    elif sid == 6124:
        sql = '''select channel, uv from src_wap_channel_uv where dt = %s;''' % (int(datetime.date.strftime(day,'%Y%m%d')))
        cur.execute(sql)
        data = cur.fetchall()
        for item in data:
            value_list.append('\t'.join([str(item[0]), str(item[1])]))
        send_list.append({'sid':sid,'sid_type':'file','date':int(datetime.date.strftime(day,'%Y%m%d')),'value':'\n'.join(value_list)})
    elif sid == 6123:
        sql = '''SELECT IFNULL(c2.`category_name`, c.`category_name`) 一级分类, c.`category_name` 二级分类, SUM(t1.uv) UV, IFNULL(SUM(t2.dd), 0) '订单', 
        IFNULL(SUM(t2.ls) DIV 1000, 0) '流水', IFNULL(SUM(t2.ls) DIV 1000, 0) / SUM(t1.uv) AS '成单率', IFNULL(SUM(t2.ls) DIV 1000/SUM(t2.dd), 0) AS '客单价' 
        FROM (SELECT IFNULL(e.id, 118) entity_id, SUM(uv) uv FROM rpt_www_pvuv a LEFT JOIN dim_cid_entity e ON a.name = e.cid WHERE `date` = %s 
        AND `type` = 4 AND tinyurl = '' AND area_id = 0 GROUP BY entity_id) t1 LEFT JOIN (SELECT IFNULL(e.id, 118) entity_id, COUNT(1) dd, SUM(total_money) ls 
        FROM    r_order_base o LEFT JOIN dim_cid_entity e ON o.c_id = e.cid WHERE     loaddate = %s AND platform_type = 0 AND user_id <> 1376902545266137 
        GROUP BY entity_id) t2 ON t1.entity_id = t2.entity_id JOIN dim_r_cid_category r ON t1.entity_id = r.`c_id` JOIN dim_cid_category c ON r.`category_id` = c.`id` 
        LEFT JOIN dim_cid_category c2 ON c.`parent_id` = c2.`id` GROUP BY 一级分类, 二级分类;
        ''' % (int(datetime.date.strftime(day,'%Y%m%d')),int(datetime.date.strftime(day,'%Y%m%d')))
        cur.execute(sql)
        data = cur.fetchall()
        for item in data:
            value_list.append('\t'.join([str(item[0]), str(item[1]), str(item[2]), str(item[3]), str(item[4]), str(item[5]), str(item[6])]))
        send_list.append({'sid':sid,'sid_type':'file','date':int(datetime.date.strftime(day,'%Y%m%d')),'value':'\n'.join(value_list)})
    elif sid == 6140:
        sql = '''select b.category_name_1 as '一级品类', b.category_name_2 as '二级品类', sum(a.gross_profit)/1000 as '毛收入', sum(a.gross_profit)/sum(total_money) as '毛利率' 
        from rpt_day_deal a left join rpt_stat_all_deal b on a.deal_id = b.deal_id where date = %s and b.is_local = 1;''' % (int(datetime.date.strftime(day,'%Y%m%d')))
        cur.execute(sql)
        data = cur.fetchall()
        for item in data:
            value_list.append('\t'.join([str(item[0]), str(item[1]), str(item[2]), str(item[3])]))
        send_list.append({'sid':sid,'sid_type':'file','date':int(datetime.date.strftime(day,'%Y%m%d')),'value':'\n'.join(value_list)})
    print send_list
    values = {
              'token':'n1xb053wjhqft2ri',
              'rid':5,
              'content':json.dumps(send_list, ensure_ascii=False)
              }
    data = urllib.urlencode(values)
    print data
    req = urllib2.Request(push_url, data)
    response = urllib2.urlopen(req)
    info_page = response.read()
    print info_page

def main(day):
    today = day
    yesterday = day-datetime.timedelta(1)
    conn = db.connect(db.niux_dw)
    conn.set_character_set('utf8')
    cur = conn.cursor()
    register_num(cur)
    push_num(yesterday,cur)
    register_file(cur)
    for sid in file_dict.iterkeys():
        push_file(yesterday,cur,sid)

if __name__ == '__main__':
#    main(datetime.date(2014,3,13))
    day = datetime.date.today()
    for i in range(3):
        main(day)
        print day
        day -= datetime.timedelta(1)
    
    
    
