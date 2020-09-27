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