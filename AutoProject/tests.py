# from django.test import TestCase
#
# # Create your tests here.
#
# # -*-coding:utf-8-*-

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
import requests
import json
#
# server_url = "http://192.168.1.121/installsmoke"
# parm = {"version": 1, "host": 2}
# data = requests.post(server_url, parm)
# vop_data = json.loads(data.content)



# import requests
# requests.post(url='http://192.168.1.120:7000/project/install/ansible',
#               json={'id': 1,
#                     'tag_version': 1,
#                     'model_version':2
#                     })
