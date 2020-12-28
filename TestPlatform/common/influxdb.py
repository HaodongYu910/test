#!/usr/bin/env python
# coding=utf-8


from django.conf import settings
import logging
from influxdb import InfluxDBClient

logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置，这里有一个层次关系的知识点。


class influxDB():
    def __init__(self):
        self.client = InfluxDBClient(host=settings.Influxdb, port='8086',database=settings.InfluxDataBase,ssl=True, verify_ssl=True) # 连接数据库
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

