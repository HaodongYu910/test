from django.test import TestCase

# Create your tests here.

# -*- coding: UTF-8 -*-
import re, urllib, json, requests

# print(str(re.findall(r"(.+?)-", 'WEB')[0]))


# -*-coding:utf-8-*-
# import os
# for root,dirs,files in os.walk("d:\\testDatas"):
#     for dir in dirs:
#         print(dir)
#         print(os.path.join(root,dir))
#         # for file in files:
#         #     print(os.path.join(root,file))
#


# dict1=[{"a":1,"b":2,"c":3},{"a":3,"b":1,"c":3},{"a":2,"b":2,"c":3}]
# dict2=[{"a":2,"b":2,"c":1},{"a":0,"b":9,"c":3},{"a":3,"b":1,"c":0}]
#
# diff = dict1.keys() & dict2
# diff_vals = [(k, dict1[k], dict2[k]) for k in diff if dict1[k] != dict2[k]]


# from multiprocessing import Pool,Process
# import time,os
# def Foo(a):#创建函数
#     for i in range(10):
#         a=a+a
#         time.sleep(1000)
#         bar()
#     return a
#
# def bar():#创建函数
#     arga=datetime.datetime.today()
#     print('---->',arga)
# if __name__ == '__main__':
#
#     pool = Pool(2)#创建进程池最大容量为2，最多允许2个进程同时运行，参照线程信号量模式
#     for i in 'Brain,CTA,CTP,Lung,MRA'.split(","):
#         pool.apply_async(func=Foo, args=(i,))
#
#     # pool.close()
#
#
#
# from multiprocessing import Process
# import os
#
# def info(tx):
#     print(datetime.datetime.today())
#     print('module name:', __name__)
#     print('parent process:', os.getppid())
#     print('process id:', os.getpid())
#
# def f(name):
#     info('function f')
#     time.sleep(10)
#     print('hello', name)
#
# if __name__ == '__main__':
#     info('main line')
#     p = Process(target=f, args=('bob',))
#     pa = Process(target=f, args=('bob',))
#     p.start()
#     p.join()
#     pa.start()


import datetime
import pandas as pd
import psycopg2 as pc
import csv
from TestPlatform.common.regexUtil import connect_to_postgres

def getcsv():
    # print(os.path.abspath(os.path.dirname(os.getcwd())))

    csv_pd = pd.read_csv("C:\\Users\\yinhang\\Desktop\\stress\\lung2.csv")
    csv = csv_pd.to_dict(orient='records')
    return csv


if __name__ == '__main__':
    patientid='0950028'
    orthanc_ip='192.168.1.208'
    vote=''
    # Series = connect_to_postgres(orthanc_ip,
    #                                  "select \"StudyInstanceUID\" from \"Study\" where \"PatientID\" ='{0}'".format(
    #                                      patientid)).to_dict(orient='records')
    # pseries_classifier = connect_to_postgres(orthanc_ip,
    #                                              "select protocol->'pseries_classifier' as \"pseries\" from hanalyticsprotocol where studyuid ='{0}' LIMIT 1;".format(
    #                                                  uid)).to_dict(orient='records')
    #
    # pseries=pseries_classifier[0]['pseries']
    # for key in pseries:
    #     for i in Series:
    #         if str(i['SeriesInstanceUID']) in str(pseries[key]):
    #             vote= vote+'{0}: \\"{1}\\",'.format(str(key),str(i['SeriesInstanceUID']))
    # vote="{"+vote+"}"
    print(vote)

