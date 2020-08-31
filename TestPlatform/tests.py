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
import os
for root,dirs,files in os.walk("d:\\testDatas"):
    for dir in dirs:
        print(dir)
        print(os.path.join(root,dir))
        # for file in files:
        #     print(os.path.join(root,file))

