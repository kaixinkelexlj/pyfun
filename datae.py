# !usr/bin/env python
# -*- coding:utf-8 _*-

"""
__author__ : guojiaqi
__email__ : guojiaqi@didichuxing.com
__file_name__ : modify_studio_conf.py
__create_time__ : 2020/07/20
"""
from argparse import ArgumentParser
import urllib.request
import json

DATA_CENTER_URL = "http://bigdata.xiaojukeji.com/report/v1/list/dataSourceDetail?reportId="
STUDIO_APIKEY = "d71717fdb8a7435bb26fe884c1293ee8"
STUDIO_PROJECT_CODE = "dps_data_center"
STUDIO_URL = "http://10.88.128.45/datastudio/v1/task/update"
STUDIO_USER = "hurenqiang"
SEPARATOR = "===================="

def parser_args():
    arg_parser = ArgumentParser()
    arg_parser.add_argument('--report_ids', help='datae report_ids')
    arg_parser.add_argument('--username', help='operator username')
    arg_parser.add_argument('--ddc_ticket', help='operator ddc_ticket')
    arg_parser.add_argument('--conf_field', default = "baselineId" ,help='modify field')
    arg_parser.add_argument('--conf_value', default = 2663 ,help='modify value')
    args = arg_parser.parse_args()
    if(args.report_ids is None or args.username is None or args.ddc_ticket is None):
        print("lack args, required [report_ids] [username] [ddc_ticket]")
        exit()
    return args

def request_schedule_code(report_id, username, ddc_ticket):
    url = DATA_CENTER_URL + report_id
    headers = {"Cookie" : "username={};ddc_ticket={}".format(username, ddc_ticket)}
    request = urllib.request.Request(url = url, data = None, headers = headers)
    response = urllib.request.urlopen(request)
    data_source_list = json.loads(response.read())['data']['dataSources']
    data_source_codes = set()
    for data_source in data_source_list:
        data_source_codes.add("dps_data_center.{}".format(data_source['scheduleUrlCode']))
    return data_source_codes

def request_modify_conf(studio_code , conf_field , conf_value , username):
    headers = {"apikey" : STUDIO_APIKEY, "projectCode" : STUDIO_PROJECT_CODE, "userId" : STUDIO_USER, "Content-Type": "application/json"}
    params = {"scheduleUuid" : studio_code}
    task_schedule = {conf_field : conf_value}
    params["taskSchedule"] = task_schedule
    data = bytes(json.dumps(params), 'UTF8')
    request = urllib.request.Request(url = STUDIO_URL, data = data, headers = headers)
    response = urllib.request.urlopen(request)
    print(json.loads(response.read()))
    print(SEPARATOR)

def modify_conf(report_id, username, ddc_ticket, conf_field="baselineId", conf_value = 2663):
    studio_codes = request_schedule_code(report_id, username, ddc_ticket)
    for studio_code in studio_codes:
        print("report_id[{}] studio_code[{}] conf_field[{}] conf_value[{}]".format(report_id, studio_code, conf_field , conf_value))
        request_modify_conf(studio_code, conf_field , conf_value , username)

if __name__ == '__main__':
    args = parser_args()
    report_ids = args.report_ids.strip().split(",")
    username = args.username
    ddc_ticket = args.ddc_ticket
    conf_field = args.conf_field
    conf_value = args.conf_value
    for report_id in report_ids:
        modify_conf(report_id, username, ddc_ticket, conf_field, conf_value)
