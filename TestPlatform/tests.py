from django.test import TestCase

# Create your tests here.

# -*- coding: UTF-8 -*-
import re, urllib, json, requests



# print(str(re.findall(r"(.+?)-", 'WEB')[0]))


def test():
    for j in range(20):
        server_url = "http://api.heyuedi.com/recommend/topic/list?order_by=margin&page=" + str(j) + "&coin_kind="
        vop_url_request = urllib.request.Request(server_url)
        vop_response = urllib.request.urlopen(vop_url_request)
        vop_data = json.loads(vop_response.read())

        for i in vop_data["data"]["data"]:
            print("用户", i["user"]["nickname"], "实盘收益率", i["recommend"]["current_incr_ratio"], "推荐币成功率",
                  i["user"]["success_ratio"], "推荐币收益率", i["user"]["realised_pnl_ratio"])


def testpost():
    for i in range(50):
        server_url = "http://app.bpop.vip/recommendCurrency/kolRecommendInfo"
        parm = {"page": 1, "recommendType": 2, "tokenid": 145552, "isAll": "true", "kolid": 171186}
        parm["page"] = i
        data = requests.post(server_url, parm)
        vop_data = json.loads(data.content)
        a = 0
        for j in vop_data["data"]["data"]["allKolInfo"]["resultList"]:
            print(vop_data["data"]["data"]["allKolInfo"]["resultList"][a]["kolname"],
                  "￥" + str(vop_data["data"]["data"]["allKolInfo"]["resultList"][0]["balance"]) + "元")
            a = a + 1


from TestPlatform.common.regexUtil import *



# -*-coding:utf-8-*-
# import os
# for root,dirs,files in os.walk("d:\\testDatas"):
#     for dir in dirs:
#         print(dir)
#         print(os.path.join(root,dir))
#         # for file in files:
#         #     print(os.path.join(root,file))
#


# dicta=[{"a":1,"b":2,"c":3},{"a":3,"b":1,"c":3},{"a":2,"b":2,"c":3}]
# dictb=[{"a":2,"b":2,"c":1},{"a":0,"b":9,"c":3},{"a":3,"b":1,"c":0}]
#
# for i in dicta:
#     dicta[i]["a"].find
from multiprocessing import Pool,Process
# import time,os
# def Foo(a):#创建函数
#     for i in range(10):
#         a=a+a
#         time.sleep(1)
#
#     print('process:',a,'time:',bar())
#     return a

# def bar():#创建函数
#     arga=datetime.datetime.today()
#     print('---->',arga)
# if __name__ == '__main__':
#     pool = Pool(2)#创建进程池最大容量为2，最多允许2个进程同时运行，参照线程信号量模式
#     for i in range(5):#创建10个进程
#         print('in the time:', bar())
#         pool.apply_async(func=Foo,args=(i,))#创建线程，参数1调用函数，参数2设置i为函数FOO参数，参数3为返回函数
#     pool.close() #关闭
#     print("返回成功")

