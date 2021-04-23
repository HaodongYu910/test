#! /usr/bin/python
# -*- coding:utf-8 -*-

import json, os
import pandas as pd
import psycopg2 as pc
from AutoTest.common.transport import SSHConnection
from ..models import Server
from django.conf import settings
import logging
logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置


"""
Created on

@author: vte
获取数据库密码
"""


def postgresInfo(**kwargs):
    path = settings.BASE_DIR
    try:
        ssh = SSHConnection(host=kwargs["host"], pwd=kwargs["pwd"], user=kwargs["user"])
        ssh.download('{}/cache/postgresql{}.json'.format(path, kwargs["host"]),
                     '/home/biomind/.biomind/var/biomind/orthanc/postgresql.json')
        ssh.close()
        with open("{}/cache/postgresql{}.json".format(path, kwargs["host"]), "r") as f:
            load_dict = json.load(f)
            return load_dict["PostgreSQL"]
    except Exception as e:
        logger.error(e)

# """链接数据库"""
def connect_postgres(**kwargs):
    path = settings.BASE_DIR
    HostInfo = Server.objects.get(id=kwargs["host"])
    try:
        with open("{}/cache/postgresql{}.json".format(path, HostInfo.host), "r") as f:
                load_dict = json.load(f)
                info = load_dict["PostgreSQL"]
        conn = pc.connect(database=kwargs["database"], user=info["Username"], password=info["Password"], host=HostInfo.host, port=info["Port"])
    except Exception as e:
        info = postgresInfo(host=HostInfo.host, pwd=HostInfo.pwd, user=HostInfo.user)
        conn = pc.connect(database=kwargs["database"], user=info["Username"], password=info["Password"],
                          host=HostInfo.host, port=info["Port"])
        logger.error("密码错误：重新获取{}".format(e))
    result = pd.read_sql(kwargs["sql"], conn)
    conn.close()
    return result

def connect_postgres_dicommaster(**kwargs):
    info = postgresInfo(host=kwargs["host"],pwd="biomind")
    conn = pc.connect(database="dicommaster", user=info["Username"], password=info["Password"], host=kwargs["host"], port=info["Port"])
    result = pd.read_sql(kwargs["sql"], conn)
    conn.close()
    return result


