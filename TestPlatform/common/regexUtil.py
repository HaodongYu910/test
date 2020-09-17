import re
import time
import urllib
import json
import logging,os, datetime,psutil
from datetime import timedelta
import pandas as pd
import psycopg2 as pc
from TestPlatform.utils.keycloak.keycloakclient import KeycloakClient
from influxdb import InfluxDBClient
import csv

logger = logging.getLogger(__name__)

# 判断是否是手机
def isMobile(str):
    reg = r'^1[35678]\d{9}$'
    if re.match(reg, str):
        return True
    else:
        return False


# 判断是否是邮箱
def isEmail(str):
    reg = r'^\s*[A-Za-z\d]+([-_.][A-Za-z\d]+)*@([A-Za-z\d]+[-.])+[A-Za-z\d]{2,4}\s*$'
    if re.match(reg, str):
        return True
    else:
        return False


# 判断是否工作日
def Weekdays(str):
    nTime = time.strftime('%Y%m%d', time.localtime())
    # 节假日接口
    server_url = "http://api.goseek.cn/Tools/holiday?date="
    vop_url_request = urllib.request.Request(server_url + nTime)
    vop_response = urllib.request.urlopen(vop_url_request)
    vop_data = json.loads(vop_response.read())
    # 打印返回的Json串
    if vop_data['data'] == 0:
        return True
    else:
        return False


# """链接数据库"""
def connect_to_postgres(orthanc_ip,sql):
    conn = pc.connect(database="orthanc", user="postgres", password="4a53e4f5c42fd5a31890860b204472c5", host=orthanc_ip, port="5432")
    result = pd.read_sql(sql, conn)
    conn.close()
    return result


# 登录keycloak
def use_keycloak_bmutils(server_ip, username, password):
    try:
        kc = KeycloakClient('https://{}'.format(server_ip), 'test', 'Asd@123456')
        kc.login(username, password)
        return kc
    except Exception as e:
        logger.error('Query failed: {0}'.format(e))
        return e


def get_tc_perf():
    pid = os.getpid()
    logger.info("pid: {}".format(pid))
    for proc in psutil.process_iter():
        if proc.pid == pid:
            logger.info("[PERF]# Thread, Memory(percentage) used while loading: %s, %s (%s) ",
                         proc.num_threads(), proc.memory_info(), proc.memory_percent())


# 链接InfluxDB时序数据库
def connect_to_influx(username, password, database, task_type, task_content):
    client = InfluxDBClient(host='10.100.201.111', port='8086', username=username, password=password,
                            database=database)
    if task_type == 'insert':
        result = client.write_points(task_content)
    elif task_type == 'query':
        result = client.query(task_content)

    return result


def get_current_time(time_format, time_less):
    time = datetime.now() - timedelta(hours=time_less)
    #     time = pd.to_datetime(time)
    cur_time = time.strftime(time_format)

    return cur_time


# 读取csv数据
def getcsv(csvname):
    # print(os.path.abspath(os.path.dirname(os.getcwd())))
    ospath = os.getcwd() + "/TestData/" + csvname
    csv_pd = pd.read_csv(ospath, dtype={'studyinstanceuid': 'str'})
    csv = csv_pd.to_dict(orient='records')
    return csv

#  保存csv数据
def savecsv(data,csvname):
    with open(csvname, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(data)

#  duration 统计数据
def durationtotal(duration_all, server, aistatus):
    if int(duration_all.count()) == 0:
        return 0
    studyuid= ''
    for j in duration_all:
        studyuid = studyuid+',\''+j.studyinstanceuid+'\''
    sql = 'SELECT count(1) FROM study_view WHERE studyinstanceuid in ({0}) and aistatus in ({1})'.format(
        studyuid[1:], aistatus)
    result_1 = connect_to_postgres(server, sql)
    total = result_1.to_dict(orient='records')
    return int(total[0]['count'])