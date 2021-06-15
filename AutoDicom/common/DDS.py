# coding=utf-8
'''
作用：
通过DDS的持续化测试监控图表。保证每个engine版本都适用当前dds的版本

参数说明：

'''
from AutoProject.common.PostgreSQL import connect_postgres
from AutoProject.models import *



class getDDSData:
     dds_dic = {}
     def getServer(self):
          getDDSServer_sql = "SELECT DISTINCT dds FROM `duration` WHERE dds is not Null"
          result_ddsServer = connect_postgres(host="192.168.1.121", sql=getDDSServer_sql)
          for i in len(result_ddsServer):
               dds_dic["server"] = {result_ddsServer[i]:""}

     def getData(self):
          self.getServer()



