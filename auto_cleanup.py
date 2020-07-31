#! /usr/bin/python
# -*- coding: UTF-8 -*-
# 文件名：auto_cleanup.py
import json
import urllib2
import os
import time

# kylin_url = "http://10.90.24.30:8085/kylin/api"
kylin_project = "dps_data_center"
data_center_url = "http://10.88.128.149:30460/turbodq_engine_metastore/cleanup/aggregationcachesta"
data_center_catalog_url = "http://10.88.128.149:30460/turbodq_engine_metastore/catalog"
database = "dps_data_center"
exclude_tables_in_kylin = []  # 不删除的Kylin表
exclude_models_in_kylin = []  # 不删除的Kylin Model
exclude_cubes_in_kylin = []  # 不删除的Kylin Cube
exclude_tables_in_hive = []  # 不删除的Hive表
drop_tables_in_hive_batch_size = 30  # 一次Hive Client启动删除多少表
stop_hour = 23  # 如果当前小时超过该值，则停止执行


# 获得待清楚的Kylin表、Kylin Model和Kylin Cube以及Hive表
def query_elements_to_cleanup(elements_to_cleanup_url, catalog, schema):
    headers = {"Content-Type": "application/json;charset=UTF-8"}
    request = urllib2.Request("%s/%s/%s" % (elements_to_cleanup_url, catalog, schema), None, headers)
    response = urllib2.urlopen(request)
    response_json = json.loads(response.read())
    return response_json


def query_kylin_meta(catalog):
    kylin_meta = {}
    headers = {"Content-Type": "application/json;charset=UTF-8"}
    request = urllib2.Request(data_center_catalog_url + "?catalogName=" + catalog, None, headers)
    response = urllib2.urlopen(request)
    response_json = json.loads(response.read())
    kylin_connection_info = response_json["connectionInfo"]
    kylin_connection_info_json = json.loads(kylin_connection_info)
    kylin_meta["url"] = kylin_connection_info_json["apiUrl"]
    kylin_meta["username"] = kylin_connection_info_json["userName"]
    kylin_meta["password"] = kylin_connection_info_json["password"]
    return kylin_meta


# 产生清理命令
def generate_kylin_command(cubes_in_kylin_to_cleanup, models_in_kylin_to_cleanup, tables_in_kylin_to_cleanup,
                           kylin_meta):
    kylin_result = []

    print "【需要清理的cubes, 一共 ", len(cubes_in_kylin_to_cleanup), " 个】"
    if len(cubes_in_kylin_to_cleanup):
        for i in cubes_in_kylin_to_cleanup:
            if i.lower() not in exclude_cubes_in_kylin:
                print i
                kylin_result.append(
                    "curl --connect-timeout 60 -m 1200 -X DELETE -u %s:%s \"%s/cleans/%s\"" % (
                        kylin_meta["username"], kylin_meta["password"], kylin_meta["url"], i))

    print "【需要清理的models, 一共 ", len(models_in_kylin_to_cleanup), " 个】"
    if len(models_in_kylin_to_cleanup):
        for i in models_in_kylin_to_cleanup:
            if i.lower() not in exclude_models_in_kylin:
                print i
                kylin_result.append(
                    "curl --connect-timeout 60 -m 1200 -X DELETE -u %s:%s \"%s/models/%s\"" % (
                        kylin_meta["username"], kylin_meta["password"], kylin_meta["url"], i))
    print "【需要清理的tables, 一共 ", len(tables_in_kylin_to_cleanup), " 个】"
    if len(tables_in_kylin_to_cleanup):
        for i in tables_in_kylin_to_cleanup:
            if i.lower() not in exclude_tables_in_kylin:
                print i
                kylin_result.append("curl --connect-timeout 60 -m 1200 -X DELETE -u %s:%s \"%s/tables/%s/%s\""
                                    % (kylin_meta["username"], kylin_meta["password"], kylin_meta["url"],
                                       database + "." + i, kylin_project))

    return kylin_result


def generate_hive_command(tables_in_hive_to_cleanup):
    hive_result = []
    print "【需要清理的tables, 一共 ", len(tables_in_hive_to_cleanup), " 个】"
    if len(tables_in_hive_to_cleanup):
        command_split = "hive -e \"set mapred.job.queue.name=root.dataplatform-system_prod_dps_data_center;"
        for index, value in enumerate(tables_in_hive_to_cleanup):
            if value.lower() not in exclude_tables_in_hive:
                print value
                command_split_table = command_split + ("drop table %s;" % (database + "." + value + "\""))
                command_split_view = command_split + ("drop view %s;" % (database + "." + value + "\""))
                hive_result.append(command_split_table)
                hive_result.append(command_split_view)
    return hive_result


# 执行命令
def execute_command(cleanup_commands, account_info, account_info_replacement):
    print "****************************开始执行命令******************************"
    if len(cleanup_commands):
        for i in cleanup_commands:
            current_hour = int(time.strftime('%H', time.localtime(time.time())))
            if current_hour == 0 or current_hour >= stop_hour:
                print "停止清理工作！"
                return
            print "--------------------------------- START COMMAND ---------------------------------"
            if account_info != "":
                print i.replace(account_info, account_info_replacement)
            else:
                print i
            print os.popen(i).read()
            time.sleep(2)  # 休眠15秒
            print "----------------------------------- END COMMAND ---------------------------------"


if __name__ == '__main__':
    elements_to_cleanup = query_elements_to_cleanup(data_center_url, "hive", "data_center_inner")
    element_to_cleanup_kylin = elements_to_cleanup["kylin"]
    element_to_cleanup_hive = elements_to_cleanup["hive"]

    print "##########################################################################################"
    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 开始清理Kylin ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    print "##########################################################################################"
    for key in element_to_cleanup_kylin:
        if isinstance(element_to_cleanup_kylin[key], dict):
            print "--------------------------------------------------------------------------------"
            print "~~~~~~~~~~~~~~~~~~~~~~~~~~ catalog ", key, " 清理开始 ~~~~~~~~~~~~~~~~~~~~~~"
            print "--------------------------------------------------------------------------------"
            child_element = element_to_cleanup_kylin[key]
            kylin_meta = query_kylin_meta(key)
            kylin_commands = generate_kylin_command(child_element["cubes"], child_element["models"],
                                                    child_element["tables"], kylin_meta)
            # print kylin_commands
            execute_command(kylin_commands, kylin_meta["username"] + ":" + kylin_meta["password"], "username:password")

    print "##########################################################################################"
    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 开始清理Hive Table ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    print "##########################################################################################"
    hive_commands = generate_hive_command(element_to_cleanup_hive["tables"])

    # print hive_commands
    execute_command(hive_commands, "", "")

    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 完成清理工作 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ "
