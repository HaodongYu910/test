#! /usr/bin/python
# -*- coding:utf-8 -*-

import json, os
import pandas as pd
import psycopg2 as pc
from AutoTest.common.transport import SSHConnection
from django.conf import settings

"""
Created on

@author: vte
获取数据库密码
"""


def postgresInfo(**kwargs):
    path = settings.LOG_PATH
    ssh = SSHConnection(host = kwargs["host"], pwd = kwargs["pwd"])
    ssh.download('{}/postgresql{}.json'.format(path, kwargs["host"]),
                 '/home/biomind/.biomind/var/biomind/orthanc/postgresql.json')
    ssh.close()
    with open("{}/postgresql{}.json".format(path,kwargs["host"]), "r") as f:
        load_dict = json.load(f)
        return load_dict["PostgreSQL"]

# """链接数据库"""
def connect_postgres(**kwargs):
    info = postgresInfo(host=kwargs["host"],pwd="biomind")
    conn = pc.connect(database="orthanc", user=info["Username"], password=info["Password"], host=kwargs["host"], port=info["Port"])
    result = pd.read_sql(kwargs["sql"], conn)
    conn.close()
    return result

def connect_postgres_dicommaster(**kwargs):
    info = postgresInfo(host=kwargs["host"],pwd="biomind")
    conn = pc.connect(database="dicommaster", user=info["Username"], password=info["Password"], host=kwargs["host"], port=info["Port"])
    result = pd.read_sql(kwargs["sql"], conn)
    conn.close()
    return result

