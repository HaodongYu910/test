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




global orthanc_port,need_result,pg_db,pg_user,pg_psw,csvname


# 数据库配置
orthanc_port="5432"
pg_db = "orthanc"
pg_user = "postgres"
pg_psw = "4a53e4f5c42fd5a31890860b204472c5"

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
    conn = pc.connect(database=pg_db, user=pg_user, password=pg_psw, host=orthanc_ip, port=orthanc_port)
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
        logging.error('Query failed: {0}'.format(e))
        return e


def get_tc_perf():
    pid = os.getpid()
    logging.info("pid: {}".format(pid))
    for proc in psutil.process_iter():
        if proc.pid == pid:
            logging.info("[PERF]# Thread, Memory(percentage) used while loading: %s, %s (%s) ",
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
    excelPath='/Users/yin/Desktop/'+csvname
    with open(excelPath, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(data)

