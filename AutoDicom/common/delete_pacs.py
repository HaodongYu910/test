# coding=utf-8
import datetime
import time

import pandas
import paramiko
import paramiko as pa
import psycopg2 as pg
from AutoProject.common.PostgreSQL import connect_postgres
from AutoProject.common.mysqlDB import *
from AutoProject.common.transport import *
from AutoProject.models import dictionary
from AutoProject.utils.keycloak.login_kc import *
import logging
from ..models import dicom

logger = logging.getLogger(__name__)
import sys
import os

sys.path.append('D:\pycharm_code\TestPlatform_2\AutoDicom\common\delete_pacs.py')
os.environ['DJANGO_SETTINGS_MODULE'] = "QualityControl.settings"


def main_delete():
    try:
        # del_date = get_del_date()
        del_date = "20210609"
        sql = "SELECT studyinstanceuid FROM \"study\" WHERE studydate = '{0}' ".format(del_date)
        results = getResultsFromDB(host="192.168.2.84", sql=sql, database="orthanc")
        logging.info("[{0}],Delete step [1], get data need to be delete success".format(datetime.datetime.now()))
        if len(results):
            delDB(del_date)
            delFolder(results)
            logging.info("[{0}],Daily delete finished".format(datetime.datetime.now()))
            return
        else:
            logging.info("[{0}],Daily delete finished, [{1}] do not have data need to be delete".format(datetime.datetime.now(), del_date))
            return
    except Exception as e:
        logging.error("[{0}],Daily delete failed, error message :[{1}] ".format(
            datetime.datetime.now(), e))

def get_del_date():
    cur_date = datetime.datetime.now()
    del_date = (datetime.datetime.now() - datetime.timedelta(days=3))
    del_date = str(del_date.year) + str(f"{del_date.month:02d}") + str(f"{del_date.day:02d}")
    return del_date


def delDB(date):
    try:
        # conn = postgresDB(ip="192.168.2.84")
        # conn.deleteDB("delete from orthanc where studydate = '{0}'".format(date), "")
        conn = pg.connect(database="orthanc", user="postgres", password="4a53e4f5c42fd5a31890860b204472c5",
                          host="192.168.2.84", port="5432")
        cursor = conn.cursor()
        cursor.execute("delete from study where studydate = '{0}'".format(date))
        conn.commit()
        logging.info("[{0}],Delete step [2], Delete DB success,Total number of rows deleted :{1}".format(datetime.datetime.now(),cursor.rowcount))
        conn.close()
    except Exception as e:
        print(e)
    # try:
    #     a = 0
    #     for i in results:
    #         if a == 0:
    #             delete_sql = "DELETE FROM study where studyinstanceuid = \'{0}\'".format(i["studyinstanceuid"])
    #             a = a + 1
    #         # elif a == len(results) - 1:
    #         #     delete_sql = delete_sql + " and studyinstanceuid = \'{0}\'".format(i["studyinstanceuid"])
    #         else:
    #             delete_sql = delete_sql + " and studyinstanceuid = \'{0}\'".format(i["studyinstanceuid"])
    #             a = a + 1
    #     print(delete_sql)
    #     return delete_sql
    # except Exception as e:
    #     print(e)


def delFolder(result):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname='192.168.2.84', port=22, username='biomind', password='biomind')
        print(result)
        for i in result:
            stdin, stdout, stderr = ssh.exec_command("sshpass -p biomind sudo rm -rf /lfs/docker/volumes/orthanc-storage/_data/header/{0} && sshpass -p biomind sudo rm -rf /lfs/docker/volumes/orthanc-storage/_data/original/{1} && sshpass -p biomind sudo rm -rf /lfs/docker/volumes/orthanc-storage/_data/png/{2}".format(i["studyinstanceuid"], i["studyinstanceuid"], i["studyinstanceuid"]))
        ssh.close()
        logging.info("[{0}],Delete step [3], Daily delete folder in linux success".format(datetime.datetime.now()))
    except Exception as e:
        print(e)


def getResultsFromDB(**kwargs):
    """
    Aim to connect to orthanc database and return the result of current sql

    :param kwargs: {"sql":"",
                    "host":"",
                    "port":"",}
    :return: result[key1][key2] (result data of current sql)
        - key1 is the column name
        - key2 is the key value of current column
    """
    ## 鏈接orthanc數據庫
    try:
        connection = pg.connect(database="orthanc",
                                user="postgres",
                                password="4a53e4f5c42fd5a31890860b204472c5",
                                host=kwargs["host"],
                                port=5432)
        result = pandas.read_sql(kwargs["sql"], connection)
        if len(result):
            result = result.to_dict(orient='record')
            connection.close()
            return result
        else:
            result = ""
            connection.close()
            return result
    except Exception as e:
        print("connec to server [{0}] failed, detail :[{1}] ".format(kwargs["host"], e))
