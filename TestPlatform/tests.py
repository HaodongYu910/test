# from django.test import TestCase
#
# # Create your tests here.
#
# # -*- coding: UTF-8 -*-
# import re, urllib, json, requests
#
# # print(str(re.findall(r"(.+?)-", 'WEB')[0]))
#
#
# # -*-coding:utf-8-*-
# # import os
# # for root,dirs,files in os.walk("d:\\testDatas"):
# #     for dir in dirs:
# #         print(dir)
# #         print(os.path.join(root,dir))
# #         # for file in files:
# #         #     print(os.path.join(root,file))
# #
#
#
# # dict1=[{"a":1,"b":2,"c":3},{"a":3,"b":1,"c":3},{"a":2,"b":2,"c":3}]
# # dict2=[{"a":2,"b":2,"c":1},{"a":0,"b":9,"c":3},{"a":3,"b":1,"c":0}]
# #
# # diff = dict1.keys() & dict2
# # diff_vals = [(k, dict1[k], dict2[k]) for k in diff if dict1[k] != dict2[k]]
#
#
# # from multiprocessing import Pool,Process
# # import time,os
# # def Foo(a):#创建函数
# #     for i in range(10):
# #         a=a+a
# #         time.sleep(1000)
# #         bar()
# #     return a
# #
# # def bar():#创建函数
# #     arga=datetime.datetime.today()
# #     print('---->',arga)
# # if __name__ == '__main__':
# #
# #     pool = Pool(2)#创建进程池最大容量为2，最多允许2个进程同时运行，参照线程信号量模式
# #     for i in 'Brain,CTA,CTP,Lung,MRA'.split(","):
# #         pool.apply_async(func=Foo, args=(i,))
# #
# #     # pool.close()
# #
# #
# #
# # from multiprocessing import Process
# # import os
# #
# # def info(tx):
# #     print(datetime.datetime.today())
# #     print('module name:', __name__)
# #     print('parent process:', os.getppid())
# #     print('process id:', os.getpid())
# #
# # def f(name):
# #     info('function f')
# #     time.sleep(10)
# #     print('hello', name)
# #
# # if __name__ == '__main__':
# #     info('main line')
# #     p = Process(target=f, args=('bob',))
# #     pa = Process(target=f, args=('bob',))
# #     p.start()
# #     p.join()
# #     pa.start()
#
#
# import datetime
# import pandas as pd
# import psycopg2 as pc
# import csv
# from TestPlatform.common.regexUtil import connect_to_postgres
#
# def getcsv():
#     # print(os.path.abspath(os.path.dirname(os.getcwd())))
#
#     csv_pd = pd.read_csv("C:\\Users\\yinhang\\Desktop\\stress\\lung2.csv")
#     csv = csv_pd.to_dict(orient='records')
#     return csv
#
#
# import  pymysql
# def sqlDB(sql, data):
#     conn = pymysql.connect(host='192.168.1.121', user='root', passwd='P@ssw0rd2o8', db='autotest',
#                            charset="utf8");  # 连接数据库
#     cur = conn.cursor()
#     try:
#         cur.execute(sql, data)
#         conn.commit()
#     except Exception as e:
#         conn.rollback()
#     cur.close()
#     conn.close()
#     return data
#
# if __name__ == '__main__':
#     import csv,os
#     import pandas as pd
#     # 读取csv数据
#     def getcsv(csvname):
#         # print(os.path.abspath(os.path.dirname(os.getcwd())))
#         csv_pd = pd.read_csv(csvname, dtype={'studyinstanceuid': 'str'})
#         csv = csv_pd.to_dict(orient='records')
#         return csv
#     data=getcsv('C:\\Users\\yinhang\\Desktop\\Golden.csv')
#     uid =''
#     vote =''
#     r= ''
#     ser=''
#     for i in data:
#         if uid == i['StudyUID']:
#             vote =vote+"{0}: \"{1}\",".format(i['SeriesDescription'],i['SeriesInstanceUID'])
#         else:
#             vote = "{" + vote + "}"
#             if uid != '':
#                 sql='UPDATE  dicom set vote=\''+str(vote)+'\',diagnosis=\''+str(r)+'\' where studyinstanceuid =\''+str(uid)+'\''
#                 sqlDB(sql, [])
#             uid = i['StudyUID']
#             r = i['Restult']
#             if i['SeriesDescription'] =='CT_Lung':
#                 ser ='Lung'
#             elif i['SeriesDescription'] =='HEAD NECKCTA':
#                 ser ='Neck'
#             elif i['SeriesDescription'] =='CT_Brain':
#                 ser ='Brain'
#             else:
#                 ser = i['SeriesDescription']
#             vote = "{0}: \"{1}\",".format(i['SeriesDescription'], i['SeriesInstanceUID'])
#

# csvname='C:\\Users\\yinhang\\Desktop\\test.csv'
#                 csv_pd = pd.read_csv(csvname, dtype={'studyinstanceuid': 'str'})
#                 csv = csv_pd.to_dict(orient='records')
#                 for i in csv:
#                     obj = dicom.objects.get(studyinstanceuid=i['StudyUID'],type='Gold')
#                     obj.diagnosis = i['Restult']
#                     obj.save()


