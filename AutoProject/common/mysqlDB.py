#!/usr/bin/env python
#coding=utf-8

# import redis
# import time
# import os
# from datetime import date
import logging
import pymysql
import pandas as pd
import psycopg2 as pc
from django.conf import settings
import logging
from influxdb import InfluxDBClient

logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置，这里有一个层次关系的知识点。


class mysqlDB():
    def __init__(self):
        self.conn = pymysql.connect(host='192.168.2.38', user='', passwd='',db='', charset="utf8");  # 连接数据库
        self.cur = self.conn.cursor()

    def selectDB(self,parameter):
        # 查询数据
        cr = self.cur.execute(parameter) # 查询
        data = self.cur.fetchmany(cr)
        self.conn.commit()
        self.cur.close()
        self.conn.close()
        return (data)

    def insertDB(self,sql,data):
        # 多条插入数据
        try:
            self.cur.executemany(sql,data)
            self.conn.commit()
        except:
            self.conn.rollback()
        self.cur.close()
        self.conn.close()
        return (data)

    def updateDB(self,sql,data):
        # 修改或插入数据
        try:
            self.cur.execute(sql, data)
            self.conn.commit()
        except:
            self.conn.rollback()
        self.cur.close()
        self.conn.close() #关闭连接，释放资源
        return (data)

    def deleteDB(self,sql,data):
        # 删除数据
        try:
            self.cur.execute(sql, data)
            self.conn.commit()
        except:
            self.conn.rollback()
        self.cur.close()
        self.conn.close() #关闭连接，释放资源
        return (data)


class postgresDB():
    def __init__(self, **kwargs):
        self.conn = pc.connect(database="orthanc", user="postgres", password="4a53e4f5c42fd5a31890860b204472c5", host=kwargs["ip"], port="5432");  # 连接数据库
        self.cur = self.conn.cursor()

    def select(self,parameter):
        # 查询数据
        result = pd.read_sql(parameter,  self.conn)
        self.conn.close()
        return result

    def insert(self,sql,data):
        # 多条插入数据
        try:
            self.cur.executemany(sql,data)
            self.conn.commit()
        except:
            self.conn.rollback()
        self.cur.close()
        self.conn.close()
        return (data)

    def updateDB(self,sql,data):
        # 修改或插入数据
        try:
            self.cur.execute(sql, data)
            self.conn.commit()
        except:
            self.conn.rollback()
        self.cur.close()
        self.conn.close() #关闭连接，释放资源
        return (data)

    def deleteDB(self,sql,data):
        # 删除数据
        try:
            self.cur.execute(sql, data)
            self.conn.commit()
        except:
            self.conn.rollback()
        self.cur.close()
        self.conn.close() #关闭连接，释放资源
        return data

#
class influxDB():
    def __init__(self):
        self.client = InfluxDBClient(host=settings.Influxdb, port='8086',database=settings.InfluxDataBase,ssl=True,verify_ssl=True) # 连接数据库
        # self.client.create_database('database_name')
    def selectDB(self,parameter):
        # 查询数据
        try:
            result = self.client.query(parameter)
        except:
            logger.error("insertDB")
        self.client.close()
        return result

    # 插入数据
    def insertDB(self,parameter):

        try:
            result = self.client.write_points(parameter)
        except:
            logger.error("insertDB")
        self.client.close()
        return result

    def deleteDB(self,dbname):
        # 删除数据
        try:

            self.client.drop_database(dbname)
        except:
            logger.error("deleteDB")
        self.client.close() #关闭连接，释放资源
        return True

# class redisDB():
#     def __init__(self):
#         self.pool = redis.ConnectionPool(host='r-j6ca186270518904.redis.rds.aliyuncs.com', password='bishijieRedis1')  # 实现一个连接池
#         self.r = redis.Redis(connection_pool=pool)
#
#     def selectDB(self,parameter):
#         # 查询数据
#         cr = self.cur.execute(parameter) # 查询
#         data = self.cur.fetchmany(cr)
#         self.conn.commit()
#         self.cur.close()
#         self.conn.close()
#         return (data)

# def iredis(i_redis):
#     #pool = redis.ConnectionPool(host='47.52.252.90', password='')  # 实现一个连接池
#     pool = redis.ConnectionPool(host='r-j6ca186270518904.redis.rds.aliyuncs.com', password='bishijieRedis1')  # 实现一个连接池
#     r = redis.Redis(connection_pool=pool)
#     list=r.zrange(i_redis,-1,-1)
#     if list != []:
#         aa =list[0][3:]
#         bb =aa[:-2]
#         i_list = str(bb).strip(',').split(',')
#         price_native =i_list[4][2:-1]
#     else:
#         price_native="1.00"
#     return (price_native)


# sql = 'INSERT into integral.bonus_record VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
# parameter = [
#     None,932928926,0,'0',999,2,2,2,2,7,'1562033070220','1562033070220'
#                 ]
# sql = 'update candy%s%user_assets set coin_num=%s where user_id=%s;'
# data = ['.', '2132', 3344986]

# # # sql = 'delete from admin_group where group_id=%s;'
# # # data = [21]
# # # show_id ='932928926'
# # # coin_id='QualityControl'
# sql ="select id,title  from ts_tag where type='7' and group_id='2' like \'%BTC%\'"
# # parameter =[ 'candy.user_assets', show_id[1:-1], coin_id]
# print(mysqlDB().selectDB(sql))
#
#
