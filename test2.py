# -*- coding: utf-8 -*-
import sys
from typing import List, Dict
import time
from themisjobsdk.enums.enums import EmEnv, EmSchema
from themisjobsdk.utils.kwaisql import async_submit_sql
from themisjobsdk.utils.kwaisql import MyHandler
from themisjobsdk.kwaisql.kwaisql import KwaiSQL
from datetime import datetime, date, timedelta
import uuid
from themisjobsdk.enums.enums import EmProfile # 权限中心相关参数
from dsc.client import DscAccessTokenProvider

# 定义变量
APP_KEY_PROD: str = "8E8B8A22620A4024844ECD7DC5305336"  # appKey
APP_SECRET_PROD: str = "0C6D81A471594FE485A0301C665C4FEE"  # appSecret
GROUP_ID: int = 882  # 青藤项目id，需要使用自己项目id
USER: str = "liuhongliang"  # 需要使用自己的邮箱前缀

principal: str = "ad_ms/project@kuaishou.com" # "权限中心申请的principal"
authType: str = "PROJECT" # "权限中心的鉴权类型：USER、PROJECT、PROXY"
secretKey: str = "a7053b3f266e4feeb78cf2eeecc71f72" # "权限中心申请的secretKey"
authToken: str = DscAccessTokenProvider.get_token(principal, secretKey) # "根据权限中心SDK生成的token"
# authToken: str = DscAccessTokenProvider.get_token_with_time(principal, secretKey, expireMilliSecs)
queryId: str = "CDP_" + str(uuid.uuid1()) # "自定义queryId" 自定义唯一的queryId 例如"业务标记"_"UUID"

jobUserParams: dict = {}
jobUserParams[EmProfile.KUAISHOU_BIGDATA_JOB_AUTHC_PRINCIPAL.value] = principal
jobUserParams[EmProfile.KUAISHOU_BIGDATA_JOB_AUTHC_TYPE.value] = authType
jobUserParams[EmProfile.KUAISHOU_BIGDATA_JOB_AUTHC_TOKEN.value] = authToken
jobUserParams[EmProfile.KUAISHOU_BIGDATA_JOB_CUSTOM_QUERY_ID.value] = queryId


def query_hive(query):
    try:
        my_handler = MyHandler()
        KwaiSQL.builder.schema(EmSchema.hive).sql(query).user(USER).groupId(GROUP_ID).env(
            EmEnv.prod.env).appKey(APP_KEY_PROD).appSecret(APP_SECRET_PROD).massDataQuery(True).massDataQueryLimit(
            10000000).handler(my_handler).jobUserParams(jobUserParams).build().async_submit_sql()
        # 如果需要异步查询的全部结果同步返回，则增加下面判断逻辑；不需要同步返回，则去掉，自行在handler里分批处理结果
        while not my_handler.could_return:
            time.sleep(1)
        return my_handler.all_results
    except Exception:
        print(query)
        raise Exception('query_hive error')



def run(p_date, dt):
    print("*" * 50)
    print(p_date, dt)
    sql = """select binded_user_id, user_id from ks_op_vc.dwd_ks_op_certification_bind_df where p_date='{p_date}' and status=2
    """.format(p_date=p_date)
    print(sql)
    rows = query_hive(sql)
    user_map = {}
    for row in rows:
        s = user_map.get(row.get('binded_user_id'), set())
        s.add(row.get('user_id'))
        user_map[row.get('binded_user_id')] = s

    users = []
    sql = """
    select
        cdp_corporation_id,
        user_id
    from (
        select
            cdp_corporation_id,
            cdp_license
        from ad_ms.dim_cdp_ind_brand_corporation_info_all
        where p_date='{p_date}'
        group by
            cdp_corporation_id,
            cdp_license
    ) a join (
        SELECT
            user_id,
            get_json_object(brand_info, '$.licenseCode') as license
       FROM ks_db_origin_v2.gitshow_account_certification_info_dt_snapshot
       WHERE dt= '{dt}'
    ) b on a.cdp_license=b.license
    """.format(p_date=p_date, dt=dt)
    print(sql)
    rows = query_hive(sql)
    for row in rows:
        users.append((row.get('cdp_corporation_id'), row.get('user_id')))

    result = {}
    for (corporation_id, user) in users:
        son = user_map.get(user)
        if not son or len(son) == 0:
            continue
        son_set = set()
        son_set.union(son)
        son_level = son_set
        for i in range(0, 9):
            tmp = set()
            for u in son_level:
                s = user_map.get(u)
                if s:
                    tmp.add(s)
            son_level = tmp
            son_set.union(son_level)
        result[user] = son_set
    sql = """
    insert overwrite table ad_ms.dim_cdp_ind_server_user_all partition(p_date='{p_date}')
    values {values};
    """
    values = []
    for (corporation_id, b_user) in users:
        v = result.get(b_user, [])
        if len(v) == 0:
            values.append("({}, {}, {})".format(corporation_id, b_user, b_user))
        for t in v:
            values.append("({}, {}, {})".format(corporation_id, b_user, t))

    query_hive(sql.format(p_date=p_date, values=",".join(values)))


def dt_to_pdate(str):
    dt = datetime.strptime(str, '%Y-%m-%d')
    return dt.strftime('%Y%m%d')


if __name__ == '__main__':
    # yyyy-MM-dd HH:mm:ss
    biz_date = sys.argv[1]
    dt = biz_date[0:10]
    p_date = dt_to_pdate(dt)
    run(p_date, dt)